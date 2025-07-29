import os
import sys
import time
from pathlib import Path

import selenium.common
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow

from utils import load_yml, time_split, resource_path

from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec




class Uploading(QThread):
    finished = pyqtSignal(str)  # Signal to notify when the task is done
    show_injury_window = pyqtSignal(str, str, str)
    def __init__(self, year, month, day, hour, activty_tpye, workout, intensity, activity_sub_type,
                 total_time, distance, units, climb, shoes, avg_hr, max_hr, resting_hr, sleep, weight, description, injured, sick, rest_day, injury_data):
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
        self.config = load_yml(f"{Path.home()}/Library/Application Support/PolarAttack/config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

        self.wait_loop = QEventLoop()

    def run(self):
        # Perform the background task
        result = self.upload_to_attackpoint()
        # Emit the result
        self.finished.emit(result)


    def upload_to_attackpoint(self):
        chrome_binary = resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium")
        driver_path = resource_path("chromedriver")
        options = Options()
        options.binary_location = chrome_binary
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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

            except:
                pass
        else:
            submit_click()

        #wait until done I think
        #WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, "//h2[text()=\'Training\']")))
        self.driver.quit()
        return "Siker"

    def injury_upload(self, data):

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
        return "Siker"


    def injury_no_thanks(self):
        self.driver.find_element(By.XPATH, "//a[@class=\'btn\' and text()=\'No thanks\']").click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "logbody")))
        self.driver.quit()
        return "Siker"


class GetShoes(QThread):
    ready = pyqtSignal(list, list)
    def __init__(self):
        super().__init__()
        self.driver = None
        self.config = load_yml(f"{Path.home()}/Library/Application Support/PolarAttack/config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

    def run(self):
        chrome_binary = resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium")
        driver_path = resource_path("chromedriver")
        options = Options()
        options.binary_location = chrome_binary
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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
        shoes_sports = load_yml(Path.home() / "Library" / "Application Support" / "PolarAttack" / "shoes_sports.yml")
        shoes = shoes_sports['shoes']
        new = list(set(shoes_on_ap)-set(shoes))
        old = list(set(shoes)-set(shoes_on_ap))
        #return
        self.driver.quit()
        self.ready.emit(new, old)


class GetSpotrs(QThread):
    ready = pyqtSignal(list, list)
    def __init__(self):
        super().__init__()
        self.driver = None
        self.config = load_yml(f"{Path.home()}/Library/Application Support/PolarAttack/config.yml")
        self.ap_username = self.config['ap_username']
        self.password = self.config['ap_passw']

    def run(self):
        chrome_binary = resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium")
        driver_path = resource_path("chromedriver")
        options = Options()
        options.binary_location = chrome_binary
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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
        #navigate to activity types settings
        self.driver.find_element(By.XPATH, '//a[@href=\"/usermenu.jsp\" and text()=\"Settings\"]').click()
        self.driver.find_element(By.XPATH, '//a[@href=\"/editactivitytypes.jsp\"]').click()
        #bs4
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('tbody')
        rows = table.find_all('tr')[1:]

        activitys_on_ap = []
        for row in rows:
            td = row.find_all('td')
            data = td[2].find('input').get('value')
            activitys_on_ap.append(data)
        shoes_sports = load_yml(Path.home() / "Library" / "Application Support" / "PolarAttack" / "shoes_sports.yml")
        sports = shoes_sports["sports"]
        new = list(set(activitys_on_ap) - set(sports))
        old = list(set(sports) - set(activitys_on_ap))
        #
        self.driver.quit()
        self.ready.emit(new, old)

a = GetShoes()
a.run()