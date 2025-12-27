import sys
from utils import load_yml, dump_yaml, APP_DIR, sep
from PyQt5.QtWidgets import (QApplication, QWizard, QWizardPage, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QPixmap, QFont

from user_registration import start_register_async

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

        # explicit visible page title (styled)
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
