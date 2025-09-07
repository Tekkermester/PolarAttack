import appdirs

app_name = "PolarAttack"

APP_DIR = appdirs.user_data_dir(app_name, roaming=True)
CACHE_DIR =appdirs.user_cache_dir(app_name)
LOG_DIR = appdirs.user_log_dir(app_name)