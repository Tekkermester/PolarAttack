from PyQt5.QtCore import QThread, pyqtSignal
from utils import load_yml, dump_yaml, APP_DIR, LOG_DIR
import time

class Shoes(QThread):
    def __init__(self, no:str, data:list, parent=None):
        super().__init__(parent)
        self.no = no
        self.data = data
        self.filename = f"{APP_DIR}shoes_sports.yml"
    def run(self):
        try:
            sp_yaml = load_yml(self.filename)

            if self.no == "new":
                for shoe in self.data:
                    sp_yaml['shoes'].append(shoe)
                dump_yaml(self.filename, sp_yaml)
            else:
                for shoe in self.data:
                     sp_yaml['shoes'].remove(shoe)
                dump_yaml(self.filename, sp_yaml)
        except Exception as e:
            with open(f"{LOG_DIR}{time.strftime("%Y.%m.%d-%H:%M:%S")}.log","w") as log:
                log.write(str(e))


class Sports(QThread):
    def __init__(self, no,data:list, parent=None):
        super().__init__(parent)
        self.no = no
        self.data = data
        self.filename = f"{APP_DIR}shoes_sports.yml"
    def run(self):
        try:
            sp_yaml = load_yml(self.filename)

            if self.no == "new":
                for sport in self.data:
                    sp_yaml['sports'].append(sport)
                dump_yaml(self.filename, sp_yaml)
            else:
                for sport in self.data:
                    sp_yaml['sports'].remove(sport)
                dump_yaml(self.filename, sp_yaml)
        except Exception as e:
            with open(f"{LOG_DIR}{time.strftime("%Y.%m.%d-%H:%M:%S")}.log", "w") as log:
                log.write(str(e))

