import appdirs
import platform
import sys
import os

app_name = "PolarAttack"

APP_DIR = appdirs.user_data_dir(app_name, roaming=True, appauthor=False)
CACHE_DIR =appdirs.user_cache_dir(app_name, appauthor=False)
LOG_DIR = appdirs.user_log_dir(app_name, appauthor=False)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def chromium_path():
    if platform.system() == "Darwin": #MacOS
        return resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium"), resource_path("chromedriver")
    else:
        return resource_path("chromium_win\\chrome.exe"), resource_path("chromedriver.exe") #windows version

def sep()-> str:
    if platform.system() == "Windows":
        return '\\'
    else:
        return '/'
