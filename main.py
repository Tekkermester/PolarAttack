import sys
from GUI import UiMainWindow, LoadingWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

def main():
    app = QApplication(sys.argv)

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

    # Perform the setupUi function
    if ui.setupUi(main_window) == 0:
        # Hide the LoadingWindow and show the main window
        loading_window.hide()

        main_window.show()
        main_window.raise_()
        main_window.activateWindow()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
