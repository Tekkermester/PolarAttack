import appdirs
import platform
from utils import resource_path

app_name = "PolarAttack"

APP_DIR = appdirs.user_data_dir(app_name, roaming=True)
CACHE_DIR =appdirs.user_cache_dir(app_name)
LOG_DIR = appdirs.user_log_dir(app_name)

def chromium_path():
    if platform.system() == "Darwin": #MacOS
        return resource_path("chromium_mac/Chromium.app/Contents/MacOS/Chromium"), resource_path("chromedriver")
    else:
        return None, None # windows version
