import json
import requests
import time
from pathlib import Path
import os
from utils import load_yml

class Flow:
    def __init__(self):
        self.APP_NAME = "PolarAttack"
        self.home_dir = Path.home()

        self.SUPPORT_DIR = self.home_dir / "Library" / "Application Support" / self.APP_NAME
        self.CACHE_DIR = self.home_dir / "Library" / "Caches" / self.APP_NAME
        self.LOG_DIR = f"{self.home_dir}/Library/Logs/{self.APP_NAME}"

        #if folder doesn't exist
        os.makedirs(self.SUPPORT_DIR, exist_ok=True)
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)

        try:
            self.accestoken = load_yml(f"{self.SUPPORT_DIR}/tokens.yml")['accestoken']
        except FileNotFoundError:
            self.accestoken = " "

    def get_trainings(self):
        try:
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.accestoken}'
            }
            params = {
                'samples' : 'true',  #sample_type 3 -> altitude
                'route' : 'false',
                'zones' : 'false'
            }
            r = requests.get('https://www.polaraccesslink.com/v3/exercises', headers=headers, params=params, timeout=60)

            if 200 <= r.status_code < 400:
                file_name = time.strftime("%Y.%m.%d-%H:%M:%S")
                j = sorted(r.json(), key=lambda x: x["start_time"], reverse=True)
                file = json.dumps(j, indent=4)
                with open(f"{self.CACHE_DIR}/{file_name}.json","w") as jso:
                    jso.write(file)

                return f"{file_name}.json", r.status_code, None
            else:
                return None, r.status_code, None
        except requests.exceptions.ConnectionError:
            return None, None, "connection_error"
        except requests.exceptions.Timeout:
            return None, None, "timeout_error"
        except requests.exceptions.RequestException as e:
            with open(f"{self.LOG_DIR}/{time.strftime("%Y.%m.%d-%H:%M:%S")}.log","w") as log:
                log.write(str(e))
            return None, None, e