import sys
from utils import load_yml
from paths import APP_DIR, sep
from PyQt5.QtGui import QIcon

from GUI import UiMainWindow, LoadingWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./ui/icons/window_logo.png'))

    # Show the LoadingWindow
    loading_window = QMainWindow()
    loading_ui = LoadingWindow()
    loading_ui.setupUI(loading_window)
    loading_window.show()
    loading_window.raise_()
    loading_window.activateWindow()
    # Process events to ensure the LoadingWindow is displayed
    app.processEvents()

    # Initialize the main window
    main_window = QMainWindow()
    ui = UiMainWindow()
    #app.setAttribute(Qt.AA_EnableHighDpiScaling)

    # Perform the setupUi function
    if ui.setupUi(main_window) == 0:
        # Hide the LoadingWindow and show the main window
        loading_window.hide()

        main_window.show()
        main_window.raise_()
        main_window.activateWindow()

    sys.exit(app.exec_())

# Enable high DPI scaling
#os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

config: dict = load_yml(f"{APP_DIR}{sep()}config.yml")

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    if config['first_use']:
        pass#start first use process
    else:
        main()
