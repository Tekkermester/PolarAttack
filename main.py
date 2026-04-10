import sys
import os
from utils import load_yml, dump_yaml
from paths import APP_DIR, sep, resource_path
from PyQt5.QtGui import QIcon
from first_use import FirstRunWizard, create_folders
# Defer importing the GUI module until after we set the working directory in main()
from PyQt5.QtWidgets import QApplication, QMainWindow, QWizard
from PyQt5 import QtWidgets, QtCore

def main():
    # When running from a bundled application (PyInstaller), make the bundle's
    # resource directory the working directory so relative paths (e.g. ui/icons/...)
    # resolve correctly. resource_path('.') will return the bundle temp dir when frozen,
    # or the project dir when running from source.
    try:
        os.chdir(resource_path('.'))
    except Exception:
        # If resource_path(.) is not available or chdir fails, continue without crashing.
        pass
    from GUI import LoadingWindow, UiMainWindow

    app = QApplication(sys.argv)
    # Use resource_path to load the icon so it works both when running from source
    # and when packaged by PyInstaller.
    app.setWindowIcon(QIcon(resource_path('ui/icons/window_logo.png')))
    app.setApplicationName("PolarAttack")

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


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    try:
        config: dict = load_yml(f"{APP_DIR}{sep()}config.yml")
        if config['first_use']:
            create_folders()
            wizard = FirstRunWizard()
            if wizard.exec_() == QWizard.Accepted:
                config['first_use'] = False
                dump_yaml(f"{APP_DIR}{sep()}config.yml", config)
            else:
                sys.exit(0)  # user cancelled setup
        else:
            pass
        #run main after
        main()

    except FileNotFoundError:
        create_folders()
        wizard = FirstRunWizard()
        if wizard.exec_() == QWizard.Accepted:
            config['first_use'] = False
            dump_yaml(f"{APP_DIR}{sep()}config.yml", config)
        else:
            sys.exit(0)  # user cancelled setup
        #run main after
        main()
