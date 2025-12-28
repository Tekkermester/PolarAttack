import os
import sys
import time
import traceback

import selenium.common
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow

from utils import load_yml, time_split
from paths import APP_DIR, chromium_path, sep, CACHE_DIR, LOG_DIR

from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec


def kill_chromium_processes():
    """
    Attempt to terminate chromium/chrome and chromedriver processes.
    Tries psutil if available, otherwise uses platform-specific commands.
    Returns a list of (name, pid) tuples that were terminated (best-effort).
    """
    killed = []
    try:
        import psutil
    except Exception:
        psutil = None

    patterns = ('chromedriver', 'chromium', 'chrome', 'Google Chrome')

    if psutil:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = (proc.info.get('name') or '').lower()
                cmd = ' '.join(proc.info.get('cmdline') or []).lower()
                if any(p in name or p in cmd for p in patterns):
                    try:
                        proc.terminate()
                        killed.append((proc.info.get('name'), proc.info.get('pid')))
                    except Exception:
                        try:
                            proc.kill()
                            killed.append((proc.info.get('name'), proc.info.get('pid')))
                        except Exception:
                            pass
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        # wait a short while
        gone, alive = psutil.wait_procs([pinfo for p in psutil.process_iter()], timeout=1)
        return killed
    else:
        import platform
        import subprocess
        system = platform.system()
        try:
            if system == 'Windows':
                # try to kill chromedriver and chrome by image name
                subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                # can't enumerate PIDs reliably without psutil; return empty list
            else:
                # Unix-like: attempt pkill -f for various patterns
                subprocess.run(['pkill', '-f', 'chromedriver'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-f', 'Chromium'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-f', 'chrome'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        return killed

class Uploading(QThread):
    finished = pyqtSignal(list)  # Signal to notify when the task is done
    show_injury_window = pyqtSignal(str, str, str)
    def __init__(self, year, month, day, hour, activty_tpye, workout, intensity, activity_sub_type,
                 total_time, distance, units, climb, shoes, avg_hr, max_hr, resting_hr, sleep, weight, description, injured, sick, rest_day, injury_data, ex_id):
        super().__init__()
        self.driver = None
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.activity_type = activty_tpye
        self.workout = workout
        self.intensity = intensity
        self.activity_sub_type = activity_sub_type
        self.total_time = total_time
        self.distance = distance
        if units == 'km':
            self.units = 'kilometers'
        else:
            self.units = 'miles'
        self.climb = climb
        self.shoes = shoes
        self.avg_hr = avg_hr
        self.max_hr = max_hr
        self.resting_hr = resting_hr
        self.sleep = sleep
        self.weight = weight
        self.description = description
        self.injured = injured
        self.sick = sick
        self.rest_day = rest_day
        self.injury_data = injury_data
        self.ex_id = ex_id #exercise's id
        self.config = load_yml(f"{APP_DIR}{sep()}config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

        self.wait_loop = QEventLoop()

        self._cancelled = False

    #if the procces cancelled
    def cancel(self):
            """Request cancellation from the main thread. Attempts to quit driver and exit the wait loop."""
            self._cancelled = True
            try:
                # try to let the thread shut down the driver itself
                if self.driver:
                    try:
                        self.driver.quit()
                    except Exception:
                        # ignore; driver might already be dead
                        pass
            except Exception:
                pass
            try:
                if getattr(self, "wait_loop", None) is not None:
                    # exit any nested event loop so upload thread can continue/finish
                    self.wait_loop.exit()
            except Exception:
                pass

    def run(self):
        try:
        # Perform the background task
            result = self.upload_to_attackpoint()
            # Emit the result
            self.finished.emit(result)
        except Exception as e:
            # handle remote disconnects / protocol errors gracefully as cancellations
            try:
                from http.client import RemoteDisconnected as _RemoteDisconnected
            except Exception:
                _RemoteDisconnected = ()
            try:
                import urllib3
                proto_err = getattr(urllib3.exceptions, "ProtocolError", None)
            except Exception:
                proto_err = None

            is_remote_disc = isinstance(e, tuple(filter(None, (_RemoteDisconnected, proto_err))))
            # Also accept textual match if library types differ
            if is_remote_disc or 'RemoteDisconnected' in str(e) or 'ProtocolError' in str(e):
                # treat as a cancelled/aborted upload
                self.finished.emit(["Cancelled", self.ex_id])
            else:
                # unexpected exception: print for debugging and emit Error
                print("Exception in Uploading thread:", e)
                traceback.print_exc()
                self.finished.emit(["Error", self.ex_id])

    def upload_to_attackpoint(self):
        chrome_binary, driver_path = chromium_path()
        options = Options()
        options.binary_location = chrome_binary
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        #options.add_argument("--user-data-dir=" + os.path.join(CACHE_DIR, "chrome_profile"))
        #options.add_argument("--disk-cache-dir=" + os.path.join(CACHE_DIR, "chrome_cache"))


        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        #login to ap
        self.driver.get("https://attackpoint.org/login.jsp")
        WebDriverWait(self.driver,10).until(ec.presence_of_element_located((By.NAME, 'username')))
        username = self.driver.find_element(By.NAME, 'username')
        username.clear()
        username.send_keys(self.ap_username)
        passw = self.driver.find_element(By.NAME,'password')
        passw.clear()
        passw.send_keys(self.password + Keys.ENTER)

        def submit_click():
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Submit']")))
            submit = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit']")
            submit.click()

        #navigate to add training
        WebDriverWait(self.driver,10).until(ec.presence_of_element_located((By.XPATH, "//h2[text()='Training']")))
        try:
            add_button = self.driver.find_element(By.XPATH, "//a[@href='/newtraining.jsp']")
        except selenium.common.NoSuchElementException:
            try:
                add_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/p[1]/a[2]")
            except selenium.common.NoSuchElementException:
                try:
                    add_button = self.driver.find_element(By.XPATH, "//a[@href='/newtraining.jsp' and text()='add training']")
                except:
                    print("Hiba törötént! :(")


        add_button.click()

        #fill the things
        WebDriverWait(self.driver,10).until(ec.presence_of_element_located((By.ID, 'session-month')))

        Select(self.driver.find_element(By.ID, 'session-month')).select_by_visible_text(self.month)
        Select(self.driver.find_element(By.ID, 'session-day')).select_by_visible_text(self.day)
        session_year = self.driver.find_element(By.ID,"session-year")
        session_year.send_keys(Keys.COMMAND + "a")
        session_year.send_keys(self.year)
        Select(self.driver.find_element(By.ID, 'sessionstarthour')).select_by_visible_text(self.hour)
        Select(self.driver.find_element(By.ID, 'activitytypeid')).select_by_visible_text(self.activity_type)
        Select(self.driver.find_element(By.ID, 'workouttypeid')).select_by_visible_text(self.workout)
        Select(self.driver.find_element(By.ID, 'intensity')).select_by_visible_text(self.intensity)
        self.driver.find_element(By.NAME, "activitymodifiers").send_keys(self.activity_sub_type)
        self.driver.find_element(By.ID, "sessionlength").send_keys(self.total_time)
        self.driver.find_element(By.ID, "distance").send_keys(self.distance)
        self.driver.find_element(By.ID, "climb").send_keys(self.climb)
        Select(self.driver.find_element(By.ID, 'distanceunits')).select_by_visible_text(self.units)
        Select(self.driver.find_element(By.NAME, 'shoes')).select_by_visible_text(self.shoes)
        self.driver.find_element(By.ID, "mhr").send_keys(self.max_hr)
        self.driver.find_element(By.ID, "ahr").send_keys(self.avg_hr)
        self.driver.find_element(By.NAME, "rhr").send_keys(self.resting_hr)
        self.driver.find_element(By.NAME, "sleep").send_keys(self.sleep)
        self.driver.find_element(By.NAME, "weight").send_keys(self.weight)
        self.driver.find_element(By.CLASS_NAME, "logtextarea").send_keys(self.description)


        #injured, rest day, sickkkk ??? why?
        if self.rest_day == Qt.Checked:
            self.driver.find_element(By.NAME, "restday").click()
            submit_click()
        if (self.injured == Qt.Checked) or (self.sick == Qt.Checked):
            if self.injured == Qt.Checked:
                self.driver.find_element(By.NAME, "injured").click()
            else:
                self.driver.find_element(By.NAME, "sick").click()
            submit_click()
            try:
                WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "injurytypeid")))
                self.show_injury_window.emit(self.year, self.month, self.day)
                self.wait_loop.exec_()
                # After event loop, handle injury data in THIS thread
                if hasattr(self, "injury_data") and self.injury_data:
                    if not self.injury_data.get("no", False):
                        self.injury_upload(self.injury_data)
                    else:
                        self.injury_no_thanks()
            except Exception:
                pass
        else:
            submit_click()

        #wait until done I think
        #WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//h2[text()=\'Training\']")))
        self.driver.quit()
        return ["Siker", self.ex_id]

    def injury_upload(self, data):
        print(self.driver.page_source)

        y = self.driver.find_element(By.ID, 'startdate-year')
        y.send_keys(Keys.COMMAND + "a")
        y.send_keys(data["year"])
        Select(self.driver.find_element(By.ID, 'startdate-month')).select_by_visible_text(data["month"])
        Select(self.driver.find_element(By.ID, 'startdate-day')).select_by_visible_text(data["day"])

        #if recoverd
        if data["recovered"]:
            self.driver.find_element(By.NAME, 'recovered').click()
            ey = self.driver.find_element(By.ID, 'enddate-year')
            ey.send_keys(Keys.COMMAND + "a")
            ey.send_keys(data["end_year"])
            Select(self.driver.find_element(By.ID, 'enddate-month')).select_by_visible_text(data["end_month"])
            Select(self.driver.find_element(By.ID, 'enddate-day')).select_by_visible_text(data["end_day"])

        Select(self.driver.find_element(By.ID, 'injurytypeid')).select_by_visible_text(data["type"])
        Select(self.driver.find_element(By.ID, 'side')).select_by_visible_text(data["side"])
        Select(self.driver.find_element(By.ID, 'severity')).select_by_visible_text(data["grade"])
        self.driver.find_element(By.XPATH, "//textarea[@name=\'description\']").send_keys(data["description"])

        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit']").click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//a[text()='record a new injury']")))
        self.driver.quit()
        return ["Siker", self.ex_id]


    def injury_no_thanks(self):
        self.driver.find_element(By.XPATH, "//a[@class=\'btn\' and text()=\'No thanks\']").click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "logbody")))
        self.driver.quit()
        return ["Siker", self.ex_id]


class GetShoes(QThread):
    ready = pyqtSignal(list, list)
    logged_in = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.driver = None
        self.config = load_yml(f"{APP_DIR}{sep()}config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

    def run(self):
        try:
            chrome_binary, driver_path = chromium_path()
            options = Options()
            options.binary_location = chrome_binary
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            #login to attackpoint
            self.driver.get("https://attackpoint.org/login.jsp")
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, 'username')))
            username = self.driver.find_element(By.NAME, 'username')
            username.clear()
            username.send_keys(self.ap_username)
            passw = self.driver.find_element(By.NAME, 'password')
            passw.clear()
            passw.send_keys(self.password + Keys.ENTER)
            try:
                error = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH,"//a[text()=\'shoes\']")))
                self.logged_in.emit(True)
            except selenium.common.exceptions.TimeoutException:
                self.logged_in.emit(False)
                self.ready.emit([],[])
                self.driver.quit()
            #navigate to shoes
            shoes_btn = self.driver.find_element(By.XPATH, "//a[text()=\'shoes\']")
            shoes_btn.click()
            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//a[@href=\'/editshoes.jsp\' and text()=\'add a new pair\']")))
            #to bs4
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            table = soup.find('table')
            rows = table.find_all('tr')[1:]
            shoes_on_ap = []
            for row in rows:
                td = row.find_all('td')
                shoes_on_ap.append(td[1].get_text(strip=True))
            #compare shoe lists
            shoes_sports = load_yml(f"{APP_DIR}{sep()}shoes_sports.yml")
            shoes = shoes_sports['shoes']
            new = list(set(shoes_on_ap) - set(shoes))
            old = list(set(shoes) - set(shoes_on_ap))
            #return
            self.driver.quit()
            self.ready.emit(new, old)
        except  Exception:
            self.ready.emit([], [])
            with open(f"{LOG_DIR}{sep()}{time.strftime("%Y.%m.%d-%H:%M:%S")}.log", "w") as log:
                log.write(str(traceback.format_exc()))


class GetSpotrs(QThread):
    ready = pyqtSignal(list, list)
    logged_in = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.driver = None
        self.config: dict = load_yml(f"{APP_DIR}{sep()}config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

    def run(self):
        try:
            chrome_binary, driver_path = chromium_path()
            options = Options()
            options.binary_location = chrome_binary
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            #login to attackpoint
            self.driver.get("https://attackpoint.org/login.jsp")



            WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.NAME, 'username')))
            username = self.driver.find_element(By.NAME, 'username')
            username.clear()
            username.send_keys(self.ap_username)
            passw = self.driver.find_element(By.NAME, 'password')
            passw.clear()
            passw.send_keys(self.password + Keys.ENTER)
            try:
                error = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, "//a[text()=\'Settings\']")))
                self.logged_in.emit(True)
            except selenium.common.exceptions.TimeoutException:
                self.logged_in.emit(False)
                self.ready.emit([],[])
                self.driver.quit()
            #navigate to activity types settings
            self.driver.find_element(By.XPATH, "//a[text()='Settings']").click()
            self.driver.find_element(By.XPATH, '//a[@href=\"/editactivitytypes.jsp\"]').click()
            #bs4
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find('tbody')
            rows = table.find_all('tr')[1:-2]

            activitys_on_ap = []
            for row in rows:
                td = row.find_all('td')
                td_2 = td[1].find('input')
                data = td_2.get('value')
                activitys_on_ap.append(data)
            shoes_sports: dict = load_yml(f"{APP_DIR}{sep()}shoes_sports.yml")
            sports = shoes_sports["sports"]
            new = list(set(activitys_on_ap) - set(sports))
            old = list(set(sports) - set(activitys_on_ap))
            #
            self.driver.quit()
            self.ready.emit(new, old)
        except Exception:
            self.ready.emit([],[])
            with open(f"{LOG_DIR}{sep()}{time.strftime("%Y.%m.%d-%H:%M:%S")}.log", "w") as log:
                log.write(str(traceback.format_exc()))
