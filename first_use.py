import sys
import os
from paths import APP_DIR, CACHE_DIR, LOG_DIR, sep
from utils import load_yml, dump_yaml, APP_DIR, sep
from PyQt5.QtWidgets import (QApplication, QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QPixmap, QFont

from user_registration import start_register_async


def create_folders():
    #create files
    os.makedirs(APP_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    #create files------
    config_template = "ap_passw:\nap_username:\nfirst_use:True\nname:\n"
    tokens_template = "accestoken:\npolar_user_id:\nmember_id:\nexpires_in:"
    shoes_sports_template = """shoes: []
    sport_dict:
      AEROBICS: null
      AGILITY: null
      AMERICAN_FOOTBALL: null
      AQUATICS: null
      BACKCOUNTRY_SKIING: null
      BADMINTON: null
      BALLET_DANCING: null
      BALLROOM_DANCING: null
      BASEBALL: null
      BASKETBALL: null
      BEACH_TENNIS: null
      BEACH_VOLLEYBALL: null
      BIATHLON: null
      BODY_AND_MIN: null
      BOOTCAMP: null
      BOXING: null
      CIRCUIT_TRAINING: null
      CLIMBING: null
      CORE: null
      CRICKET: null
      CROSS-COUNTRY_SKIING: null
      CROSS_COUNTRY_RUNNING: null
      CROSS_TRAINER: null
      CURLING: null
      CYCLING: null
      DANCING: null
      DOWNHILL_SKIING: null
      DUATHLON: null
      DUATHLON_CYCLING: null
      DUATHLON_RUNNING: null
      ESPORTS: null
      E_BIKE: null
      FIELD_HOCKEY: null
      FINNISH_BASEBALL: null
      FITNESS_BOXING: null
      FITNESS_DANCING: null
      FITNESS_MARTIAL_ARTS: null
      FITNESS_STEP: null
      FLOORBALL: null
      FREE_MULTISPORT: null
      FRISBEEGOLF: null
      FUNCTIONAL_TRAINING: null
      FUTSAL: null
      GOLF: null
      GRAVEL: null
      GROUP_EXERCISE: null
      GYMNASTICK: null
      HANDBALL: null
      HIIT: null
      HIKING: null
      ICE_HOCKEY: null
      ICE_SKATING: null
      INDOOR_CYCLING: null
      INDOOR_ROWING: null
      INLINE_SKATING: null
      JAZZ_DANCING: null
      JOGGING: null
      JUDO_MARTIAL_ARTS: null
      JUMP_ROPE: null
      KETTLEBELL: null
      KICKBIKE: null
      KICKBOXING_MARTIAL_ARTS: null
      LATIN_DANCING: null
      LES_MILLS_BARRE: null
      LES_MILLS_BODYATTACK: null
      LES_MILLS_BODYBALANCE: null
      LES_MILLS_BODYCOMBAT: null
      LES_MILLS_BODYJAM: null
      LES_MILLS_BODYPUMP: null
      LES_MILLS_BODYSTEP: null
      LES_MILLS_CXWORKS: null
      LES_MILLS_GRIT_ATHLETIC: null
      LES_MILLS_GRIT_CARDIO: null
      LES_MILLS_GRIT_STRENGTH: null
      LES_MILLS_RPM: null
      LES_MILLS_SHBAM: null
      LES_MILLS_SPRINT: null
      LES_MILLS_TONE: null
      LES_MILLS_TRIPLE: null
      MOBILITY_DYNAMIC: null
      MOBILITY_STATIC: null
      MODERN_DANCING: null
      MOTORSPORTS_CAR_RACING: null
      MOTORSPORTS_ENDURO: null
      MOTORSPORTS_HARD_ENDURO: null
      MOTORSPORTS_MOTOCROSS: null
      MOTORSPORTS_ROADRACING: null
      MOTORSPORTS_SNOCROSS: null
      MOUNTAIN_BIKING: null
      NORDIC_WALKING: null
      OBSTACLE_COURSE_RACING: null
      OFFROADDUATHLON: null
      OFFROADDUATHLON_CYCLING: null
      OFFROADDUATHLON_RUNNING: null
      OFFROADTRIATHLON: null
      OFFROADTRIATHLON_CYCLING: null
      OFFROADTRIATHLON_RUNNING: null
      OFFROADTRIATHLON_SWIMMING: null
      OPEN_WATER_SWIMMING: null
      ORIENTEERING: null
      ORIENTEERING_MTB: null
      ORIENTEERING_SKI: null
      OTHER_INDOOR: null
      OTHER_OUTDOOR: null
      PADEL: null
      PARASPORTS_HAND_CYCLING: null
      PARASPORTS_SLED_HOCKEY: null
      PARASPORTS_WATER_SKIING: null
      PARASPORTS_WHEELCHAIR: null
      PARASPORTS_WHEELCHAIR_BASKETBALL: null
      PARASPORTS_WHEELCHAIR_TENNIS: null
      PICKLEBALL: null
      PILATES: null
      POOL_SWIMMING: null
      RIDING: null
      RINGETTE: null
      ROAD_BIKING: null
      ROAD_RUNNING: null
      ROLLER_BLADING: null
      ROLLER_SKIING_CLASSIC: null
      ROLLER_SKIING_FREESTYLE: null
      ROWING: null
      RUGBY: null
      RUNNING: null
      SHOOTING_SPORT_INDOOR: null
      SHOOTING_SPORT_OUTDOOR: null
      SHOW_DANCING: null
      SKATEBOARDING: null
      SKATING: null
      SNOWBOARDING: null
      SNOWSHOE_TREKKING: null
      SOCCER: null
      SPINNING: null
      SQUASH: null
      STAIR_WORKOUT: null
      STREET_DANCING: null
      STRENGTH_TRAINING: null
      STRETCHING: null
      SUP: null
      SWIMMING: null
      TABLE_TENNIS: null
      TAEKWONDO_MARTIAL_ARTS: null
      TELEMARK_SKIING: null
      TENNIS: null
      TRACK_AND_FIELD_RUNNING: null
      TRAIL_RUNNING: null
      TREADMILL_RUNNING: null
      TRIATHLON: null
      TRIATHLON_CYCLING: null
      TRIATHLON_RUNNING: null
      TRIATHLON_SWIMMING: null
      TROTTING: null
      ULTIMATE: null
      ULTRARUNNING_RUNNING: null
      VERTICALSPORTS_OUTCLIMBING: null
      VERTICALSPORTS_WALLCLIMBING: null
      VOLLEYBALL: null
      WALKING: null
      WATERSPORTS_CANOEING: null
      WATERSPORTS_KAYAKING: null
      WATERSPORTS_KITESURFING: null
      WATERSPORTS_SAILINGSailing: null
      WATERSPORTS_SURFING: null
      WATERSPORTS_WAKEBOARDING: null
      WATERSPORTS_WATERSKI: null
      WATERSPORTS_WINDSURFING: null
      WATER_EXERCISE: null
      WATER_RUNNING: null
      XC_SKIING_CLASSIC: null
      XC_SKIING_FREESTYLE: null
      YOGA: null
    sports: []
    meghagyom: []
    """

    # App dir
    with open(f"{APP_DIR}{sep()}config.yml", "w") as config:
        config.write(config_template)
    with open(f"{APP_DIR}{sep()}shoes_sports.yml", "w") as sp:
        sp.write(shoes_sports_template)
    with open(f"{APP_DIR}{sep()}tokens.yml", "w") as tokens:
        tokens.write(tokens_template)



class FirstRunWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bejelentkezés")
        self.setWizardStyle(QWizard.ModernStyle)
        pixmap = QPixmap("ui/first_use_banner.png")
        scaled_pixmap = pixmap.scaledToWidth(250)
        self.setPixmap(QWizard.WatermarkPixmap, scaled_pixmap)

        font = QFont()
        font.setFamily("Futura")
        font.setPointSize(12)

        self.setStyleSheet(f"""
                    QWidget {{
                        background-color: rgb(24,24,24);
                        color: white;
                        font-family: {font.family()};
                        font-size: {font.pointSize()}pt;
                    }}
                    QWizard {{
                        background-color: rgb(24,24,24);
                    }}
                    QLabel {{
                        color: white;
                        font-size: {font.pointSize()}pt;
                    }}
                    QLabel#w_label {{
                        color: white;
                        font-size: {font.pointSize()+4}pt;
                    }}
                    QLineEdit {{
                        background-color: rgb(50,50,50);
                        color: white;
                        border: 1px solid orange;
                        border-radius: 5px;
                        padding: 6px;
                    }}
                    QPushButton {{
                        background-color: orange;
                        color: white;
                        border: 2px solid rgb(77,77,77);
                        border-radius: 8px;
                        padding: 6px 10px;
                        font-weight: 600;
                    }}
                    QPushButton:disabled {{
                        background-color: rgb(60,60,60);
                        color: rgb(160,160,160);
                    }}
                    QPushButton#igen_btn {{
                        background-color: gray;
                        color: rgb(160,160,160);
                    }}
                    QPushButton#polar_login {{
                        background-color: orange;
                        color: black;
                        border: none;
                        font-weight: 700;
                    }}
                    QLabel[error="true"] {{
                        color: red;
                    }}
                """)

        self.setOption(QWizard.NoBackButtonOnStartPage)
        self.setOption(QWizard.NoBackButtonOnLastPage)

        self.setButtonText(QWizard.NextButton, "Tovább >")
        self.setButtonText(QWizard.BackButton, "< Vissza")
        self.setButtonText(QWizard.FinishButton, "Kész")

        self.addPage(WelcomePage())
        self.addPage(AttackpointLogin())
        self.addPage(PolarLogin())
        self.addPage(FinalPage())

        self.resize(500, 300)
    def closeEvent(self, event):
        mb = QMessageBox(self)
        mb.setWindowTitle("Kilépés megerősítése")
        mb.setText("Biztosan ki akar lépni az alkalmazásból?")
        yes_btn = mb.addButton("Igen", QMessageBox.YesRole)
        yes_btn.setStyleSheet("background-color: gray; color: rgb(160,160,160);")
        no_btn = mb.addButton("Nem", QMessageBox.NoRole)
        mb.setDefaultButton(no_btn)
        mb.exec_()
        if mb.clickedButton() == yes_btn:
            event.accept()
        else:
            event.ignore()

class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        # keep internal header text unchanged
        self.setTitle("Kezdés")

        # explicit visible page title (styled) - uses the same string as setTitle()
        page_title = QLabel(self.title())
        page_title.setAlignment(Qt.AlignCenter)
        page_title.setStyleSheet("color: orange; font-size: 20pt; font-weight: 700;")
        page_title.setContentsMargins(0, 6, 0, 12)

        label = QLabel("PolarAttack\n\nJelentkezz be a Polarflow-ba és az Attackpointba!")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName('w_label')

        layout = QVBoxLayout()
        layout.addWidget(page_title)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)

    def initializePage(self):
        self.wizard().button(QWizard.BackButton).setVisible(False)

class AttackpointLogin(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Bejelentkezés az Attackpointba")

        # explicit visible page title (styled)
        page_title = QLabel(self.title())
        page_title.setAlignment(Qt.AlignCenter)
        page_title.setStyleSheet("color: orange; font-size: 20pt; font-weight: 700;")
        page_title.setContentsMargins(0, 6, 0, 12)

        self.username = QLineEdit()

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red")

        layout = QVBoxLayout()
        layout.addWidget(page_title)
        layout.addWidget(QLabel("Felhasználónév"))
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Jelszó"))
        layout.addWidget(self.password)

        layout.addWidget(QLabel("Jelszó megerősítése"))
        layout.addWidget(self.confirm_password)

        layout.addWidget(self.error_label)
        self.setLayout(layout)

        #  Re-check completeness on every change
        self.username.textChanged.connect(self._on_changed)
        self.password.textChanged.connect(self._on_changed)
        self.confirm_password.textChanged.connect(self._on_changed)

    def _on_changed(self):
        self.completeChanged.emit()

    def isComplete(self):
        if not self.username.text():
            self.error_label.setText("")
            return False

        if not self.password.text() or not self.confirm_password.text():
            self.error_label.setText("")
            return False

        if self.password.text() != self.confirm_password.text():
            self.error_label.setText("A két jelszó nem egyezik.")
            return False

        self.error_label.setText("")
        return True

    def validatePage(self):
        # Store values
        config_yaml: dict = load_yml(f"{APP_DIR}{sep()}config.yml")
        config_yaml["ap_username"] = self.username.text()
        config_yaml["ap_passw"] = self.password.text()
        dump_yaml(f"{APP_DIR}{sep()}config.yml", config_yaml)

        return True

class PolarLogin(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Bejelentkezés a PolarFlow-ba")

        # explicit visible page title (styled)
        page_title = QLabel(self.title())
        page_title.setAlignment(Qt.AlignCenter)
        page_title.setStyleSheet("color: orange; font-size: 20pt; font-weight: 700;")
        page_title.setContentsMargins(0, 6, 0, 12)

        self.login_button = QPushButton("Bejelentkezés")
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.login_button.clicked.connect(self.start_oauth_login)

        layout = QVBoxLayout()
        layout.addWidget(page_title)
        layout.addWidget(self.login_button)
        layout.addWidget(self.status_label)
        layout.addStretch()
        self.setLayout(layout)

        self.login_successful = False

    def initializePage(self):
        self.login_successful = False
        self.status_label.setText("")
        self.login_button.setEnabled(True)
        self.completeChanged.emit()

    def isComplete(self):
        return self.login_successful

    def start_oauth_login(self):
        self.login_button.setEnabled(False)
        self.status_label.setText("Bejelentkezés folyamatban, ne zárd be...")

        start_register_async(
            on_success=self._on_success_threadsafe,
            on_error=self._on_error_threadsafe
        )

    #
    def _on_success_threadsafe(self):
        QMetaObject.invokeMethod(self,self.oauth_finished,Qt.QueuedConnection)

    def _on_error_threadsafe(self, message):
        QMetaObject.invokeMethod(self,lambda: self.on_oauth_error(message),Qt.QueuedConnection)

    # main thread only)
    def oauth_finished(self):
        self.login_successful = True
        self.status_label.setText("Sikeres bejelentkezés ✔")
        self.completeChanged.emit()

    def on_oauth_error(self, message):
        self.login_successful = False
        self.login_button.setEnabled(True)
        self.status_label.setText(f"Hiba történt: {message}")
        self.completeChanged.emit()

class FinalPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Kész")

        page_title = QLabel(self.title())
        page_title.setAlignment(Qt.AlignCenter)
        page_title.setStyleSheet("color: orange; font-size: 20pt; font-weight: 700;")
        page_title.setContentsMargins(0, 6, 0, 12)

        label = QLabel("A beállítás sikeres!\n\nKattints a \"Kész\" gombra az indításhoz.")
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(page_title)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()

        self.setLayout(layout)

    def initializePage(self):
        self.wizard().button(QWizard.BackButton).setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = FirstRunWizard()
    wizard.show()
    sys.exit(app.exec_())
