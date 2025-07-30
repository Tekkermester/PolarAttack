import time
from datetime import date, timedelta
from fileinput import filename
from string import whitespace

from PyQt5.QtGui import QIcon, QMovie, QPixmap, QTextFrame


from utils import *
from attackpoint import Uploading, GetShoes, GetSpotrs

from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtCore import QUrl, Qt, QSize, pyqtSignal, QTimer, QObject,QRunnable,pyqtSlot, QPoint, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QListWidget, QLabel, QPushButton, QAction, \
    QListWidgetItem, QToolButton, QGridLayout, QComboBox,QHBoxLayout, QLineEdit, QFrame, QTextEdit, QMainWindow, QCheckBox, QDateEdit, \
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QDesktopWidget
from PyQt5.QtGui import QGuiApplication, QFont, QIcon
import sys
import json
from pathlib import Path

from polarflow import Flow
import webbrowser


class UiMainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.injury_window = None




    def setupUi(self, MainWindow):
        #-----------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 685)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('''
                                            QWidget#centralwidget{
                                                background-color: rgb(0,0,0)
                                            }
        ''')

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")


        #main body ------
        self.main_body = QtWidgets.QWidget(self.centralwidget)
        self.main_body.setObjectName("main_body")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.main_body)
        self.verticalLayout_3.setObjectName("verticalLayout_3")


        #top menu --------------
        self.top = QtWidgets.QWidget(self.main_body)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top.sizePolicy().hasHeightForWidth())
        self.top.setSizePolicy(sizePolicy)
        self.top.setObjectName("top")
        self.top.setStyleSheet("QWidget#top{background-color: rgb(17,17,17); border:2px solid; border-radius:10px;}")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top)
        self.horizontalLayout.setObjectName("horizontalLayout")
        #menu button
        self.menu = QtWidgets.QToolButton(self.top)
        self.menu.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu.sizePolicy().hasHeightForWidth())

        self.menu.setSizePolicy(sizePolicy)
        self.menu.setStyleSheet("background-color:transparent;\n"
                                "border-radius: 15px;")
        icon = QtGui.QIcon()  #----icon
        icon.addPixmap(QtGui.QPixmap("ui/icons/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu.setIcon(icon)
        self.menu.setIconSize(QtCore.QSize(36, 36))
        self.menu.setObjectName("menu")
        self.horizontalLayout.addWidget(self.menu)

        #settings button
        self.Settings = QtWidgets.QPushButton(self.top)
        self.Settings.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Settings.sizePolicy().hasHeightForWidth())
        self.Settings.setSizePolicy(sizePolicy)
        self.Settings.setStyleSheet("background-color:transparent;\n"
                                    "border-radius: 15px;")
        self.Settings.setText("")
        icon1 = QtGui.QIcon() #icon---
        icon1.addPixmap(QtGui.QPixmap("ui/icons/gear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Settings.setIcon(icon1)
        self.Settings.setIconSize(QtCore.QSize(30, 30))
        self.Settings.setObjectName("Settings")
        self.horizontalLayout.addWidget(self.Settings)

        #attack, polar button container
        self.top_3 = QtWidgets.QWidget(self.top)
        self.top_3.setObjectName("top_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.top_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        #attackpoint.org
        self.attckp = QtWidgets.QPushButton(self.top_3)
        self.attckp.setStyleSheet("background-color: rgb(77,77,77); border:2px solid; border-radius:10px; padding: 8px; color:white;")
        self.attckp.clicked.connect(lambda: webbrowser.open('https://attackpoint.org'))
        self.attckp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attckp.sizePolicy().hasHeightForWidth())
        self.attckp.setSizePolicy(sizePolicy)

        icon2 = QtGui.QIcon()#icon
        icon2.addPixmap(QtGui.QPixmap("ui/icons/attackpoint_400x400.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.attckp.setIcon(icon2)
        self.attckp.setObjectName("attckp")
        self.verticalLayout_2.addWidget(self.attckp)
        #flow.polar.com button
        self.polarflow = QtWidgets.QPushButton(self.top_3)
        self.polarflow.setStyleSheet("background-color: rgb(77,77,77); border:2px solid; border-radius:10px; padding:8px; color:white;")
        self.polarflow.clicked.connect(lambda: webbrowser.open('https://flow.polar.com/diary'))
        self.polarflow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.polarflow.sizePolicy().hasHeightForWidth())
        self.polarflow.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()#icon--
        icon3.addPixmap(QtGui.QPixmap("ui/icons/polar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.polarflow.setIcon(icon3)
        self.polarflow.setObjectName("polarflow")
        self.verticalLayout_2.addWidget(self.polarflow)


        self.horizontalLayout.addWidget(self.top_3, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #spacer1--
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)
        #LOGO picture
        self.logo_pic = QtWidgets.QPushButton(self.top)
        self.logo_pic.clicked.connect(lambda: webbrowser.open('https://github.com/Tekkermester/PolarAttack'))
        self.logo_pic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy.setHeightForWidth(self.logo_pic.sizePolicy().hasHeightForWidth())
        self.logo_pic.setSizePolicy(sizePolicy)
        self.logo_pic.setStyleSheet("background-color:transparent;\n"
                                    "border-radius: 15px;")
        self.logo_pic.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/icons/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logo_pic.setIcon(icon4)
        self.logo_pic.setIconSize(QtCore.QSize(70, 70))
        self.logo_pic.setObjectName("logo_pic")
        self.horizontalLayout.addWidget(self.logo_pic)

        #spacer2
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout.addItem(spacerItem1)

        #name label (def.:Regisztrálj!)
        self.name = QtWidgets.QLabel(self.top)
        self.name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(19)
        font.setBold(True)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)

        #state button
        self.state = QtWidgets.QPushButton(self.top)
        self.state.setEnabled(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.state.sizePolicy().hasHeightForWidth())
        self.state.setSizePolicy(sizePolicy)
        self.state.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.state.setStyleSheet("background-color:transparent;\n"
                                 "border-radius: 15px;")
        self.state.setText("")

        # ok.png or offline.png ------------------------
        state_icon = QtGui.QIcon()
        state_icon.addPixmap(QtGui.QPixmap("ui/icons/offline.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off) #state változó
        self.state.setIcon(state_icon)
        self.state.setIconSize(QtCore.QSize(20, 20))
        self.state.setObjectName("state")

        self.horizontalLayout.addWidget(self.state, 0, QtCore.Qt.AlignRight)

        #refresh icon --
        self.refresh = QtWidgets.QPushButton(self.top)
        self.refresh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh.sizePolicy().hasHeightForWidth())
        self.refresh.setSizePolicy(sizePolicy)
        self.refresh.setStyleSheet("background-color:transparent;\n"
                                   "border-radius: 15px;")
        self.refresh.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ui/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh.setIcon(icon6)
        self.refresh.setIconSize(QtCore.QSize(25, 25))
        self.refresh.setObjectName("refresh")
        self.refresh.clicked.connect(self.refresh_button)



        self.horizontalLayout.addWidget(self.refresh, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_3.addWidget(self.top)

        ########################################################################################################
        #bottom main body
        self.main = QtWidgets.QWidget(self.main_body)
        self.main.setObjectName("main")
        self.main_layout = QtWidgets.QHBoxLayout(self.main)
        self.main_layout.setObjectName("main_layout")

        self.verticalLayout_3.addWidget(self.main)
        self.verticalLayout.addWidget(self.main_body)
        MainWindow.setCentralWidget(self.centralwidget)


        ################## main body ###################################

        #left side ----
        self.left_groupbox = QGroupBox()
        self.left_groupbox.setObjectName("left")
        self.left_groupbox.setStyleSheet(
            "QGroupBox#left{background-color: rgb(24,24,24); border:2px solid; border-radius:10px;}")
        self.left_layout = QVBoxLayout()
        self.left_groupbox.setLayout(self.left_layout)

        ####
        self.workout_list = QListWidget()
        self.workout_list.setStyleSheet("""
            QListWidget {
                background-color: rgb(50, 50, 50);
                color: white;
            }

            QListWidget::item:selected {
                background-color: #6e6b5f;
                color: white;
            }

            QListWidget::item:hover {
                background-color: #7d7c7a;
                color: black;
            }

            QScrollBar:vertical, QScrollBar:horizontal {
                border: none;
                background: #444;
                width: 12px;
                height: 12px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #888;
                min-height: 20px;
                min-width: 20px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: orange;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                height: 0px;
                width: 0px;
            }
        """)

        self.left_layout.addWidget(self.workout_list)

        ##

        #right side -----
        self.right_groupbox = QGroupBox()
        self.right_groupbox.setObjectName("right")
        self.right_groupbox.setStyleSheet('''QGroupBox#right{
                                                    background-color: rgb(24,24,24);
                                                    border:2px solid;
                                                    border-radius:10px;
                                                    color:white;}
                                                QGroupBox#right QLabel{
                                                    color:white;
                                                    font-family: Arial;
                                                    font-weight: 700;
                                                }
                                                QGroupBox#right QComboBox {
                                                    background-color: rgb(50, 50, 50);
                                                    color: white;
                                                    border: 1px solid rgb(77, 77, 77);
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                            
                                                QGroupBox#right QComboBox QAbstractItemView {
                                                    background-color: rgb(50, 50, 50);
                                                    color: white;
                                                    selection-background-color: orange;
                                                    selection-color: black;
                                                    border: none;
                                                }
                                                QGroupBox#right QComboBox QAbstractItemView QScrollBar:vertical,
                                                QGroupBox#right QComboBox QAbstractItemView QScrollBar:horizontal {
                                                    width: 0px;
                                                    height: 0px;
                                                }
                                            
                                                QGroupBox#right QComboBox::drop-down {
                                                    background-color: orange;
                                                    border: none;
                                                    width: auto;
                                                    border-top-right-radius: 5px;
                                                    border-bottom-right-radius: 5px;
                                                }
                                            
                                                QGroupBox#right QComboBox::down-arrow {
                                                    image: url('ui/icons/down.png');
                                                    width: 20px;
                                                    height: 20px;
                                                }
                                                QGroupBox#right QLineEdit {
                                                    background-color: rgb(50, 50, 50);
                                                    font-size: 15px;
                                                    color: white;
                                                    border: 1px solid rgb(77, 77, 77);
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                    text-align: center;
                                                }
                                                QTextEdit {
                                                    background-color: rgb(77, 77, 77);
                                                    color: white;
                                                    border: 1px solid rgb(50, 50, 50);
                                                    border-radius: 5px;
                                                    padding: 5px;
                                                }
                                                QGroupBox#right QCheckBox {
                                                    color: white;
                                                    font-family: Arial;
                                                    font-size: 14px;
                                                    spacing: 5px;
                                                }
                                                QGroupBox#right QCheckBox::indicator {
                                                    width: 16px;
                                                    height: 16px;
                                                }
                                                QGroupBox#right QCheckBox::indicator:unchecked {
                                                    border: 2px solid rgb(77, 77, 77);
                                                    background-color: rgb(50, 50, 50);
                                                    border-radius: 3px;
                                                }
                                                QGroupBox#right QCheckBox::indicator:checked {
                                                    border: 2px solid orange;
                                                    background-color: orange;
                                                    border-radius: 3px;
                                                }
                                                QGroupBox#right QCheckBox::indicator:hover {
                                                    border: 2px solid white;
                                                }
                                                ''')
        self.right_layout = QVBoxLayout()
        self.right_groupbox.setLayout(self.right_layout)

        self.choose_a_tarinng_label = QLabel("<h1 style=\"color: orange;\">Válassz ki egy edzést!</h1>")
        self.choose_a_tarinng_label.show()
        self.right_layout.addWidget(self.choose_a_tarinng_label,0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #default if no selected training
        #5:7
        self.main_layout.addWidget(self.left_groupbox,6)
        self.main_layout.addWidget(self.right_groupbox,7)


        ##------##


        ############ menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        ##


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        ###################################################################################------###
        self.load_trainings()

        #--------
        ######### check for shoes and sprots if new
        self.get_shoes_worker = GetShoes()
        self.get_shoes_worker.ready.connect(self.get_shoes_finished)
        self.get_shoes_worker.start()

        self.get_sports_worker = GetSpotrs()
        self.get_sports_worker.ready.connect(self.get_sports_finished)
        self.get_sports_worker.start()






        return 0

    def get_shoes_finished(self, new: list, old: list):
        if new:
            window = NewShoeOrSport("shoes", 'new', new)
            window.show()
            window.raise_()
            window.activateWindow()
        else:
            pass
        if old:
            window = NewShoeOrSport("shoes", 'old', old)
            window.show()
            window.raise_()
            window.activateWindow()
        else:
            pass


    def get_sports_finished(self, new, old):
        if new:
            window = NewShoeOrSport("sports", 'new', new)
            window.exec_()
            window.raise_()
            window.activateWindow()
        else:
            pass
        if old:
            window = NewShoeOrSport("sports", 'old', old)
            window.exec_()
            window.raise_()
            window.activateWindow()
        else:
            pass

    def load_trainings(self):
        flow_instance = Flow()
        delete_caches(flow_instance.CACHE_DIR)

        name, status_code, error = flow_instance.get_trainings()
        #error
        if error is not None:
            if error == "connection_error":
                self.choose_a_tarinng_label.setText("<h1 style=\"color: red;\">Hiba történt!<h1>\n<h3>Ellenőrizd az internet kapcsolatot!</h3>")
            elif error == "timeout_error":
                self.choose_a_tarinng_label.setText("<h1 style=\"color: red;\">Időtúllépés :(<h1>\n<h3>Ellenőrizd az internet kapcsolatot!</h3>")
            else:
                log_dir = QUrl.fromLocalFile(flow_instance.LOG_DIR).toString()
                self.choose_a_tarinng_label.setText(f'<h1 style=\"color: red;\"><>Hiba történt :(</h1><a href="{log_dir}">Log</a>')
                self.choose_a_tarinng_label.setOpenExternalLinks(True)
        #http error
        elif name is None:
            self.choose_a_tarinng_label.setText(f"<h2 style=\"color: red;white-space: pre-line;\">{http_respons(status_code)}</h2>")
        #success ------ - - - - -- --- - -
        else: ###########
            with open(f"{flow_instance.CACHE_DIR}/{name}") as j:
                exercise_list = json.load(j)
            for ex in exercise_list:
                item_widget = QWidget()
                item_layout = QVBoxLayout()

                #altitude data ----
                for i in ex['samples']:
                    if i['sample_type'] == 3:
                        data = i['data']
                        altitudes = [float(i) for i in data.split(",")]
                #time formats________--____-----__
                if time_format(ex['start_time']) == time.strftime("%m.%d"):
                    start_time = "Ma"
                elif time_format(ex['start_time']) == (date.today()- timedelta(days=1)).strftime("%m.%d"):
                    start_time = "Tegnap"
                elif time_format(ex['start_time']) == (date.today()- timedelta(days=2)).strftime("%m.%d"):
                    start_time = "Tegnapelőtt"
                else:
                    start_time = time_format(ex['start_time'])



                #labels------
                workout_label = QLabel(f"<p><b><span style=\"color:white;\">{start_time}</span></b>  <span style=\"color:white;\">|</span>  "
                                       f"<span style=\"font-weight: 800;color: orange; font-size: 17px\">{calc_duration(ex['duration'])}</span> <span style=\"color:white;\">-</span> "
                                       f"<span style=\"font-size: 18px;color:white;\">{calc_distance(ex['distance'])} km</span> "
                                       f"<span style=\"color: #a6a49f\">+{calc_altitude(altitudes)}m</span>"
                                       f"<span style=\"color:transparent;font-size:2px;\">{ex['id']}<span></p>")
                item_layout.addWidget(workout_label)

                #upload button ---
                upload_button = QPushButton()
                upload_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                upload_button.setIcon(QIcon("ui/icons/upload.png"))
                upload_button.setText('Feltöltés Attackpointra')
                upload_button.setStyleSheet("""
                    QPushButton {
                        background-color: #d68f24;
                        color: white;
                        font-weight: bold;
                        font-size: 14px;
                        border: none;
                        border-radius: 15px;
                        padding: 8px 4px;
                    }

                    QPushButton:hover {
                        background-color: #FF8C00; 
                    }

                    QPushButton:pressed {
                        background-color: #E67300;
                    }
                """)
                upload_button.setSizePolicy(upload_button.sizePolicy().hasHeightForWidth(),False)
                upload_button.adjustSize()

                upload_button.clicked.connect(lambda _, w=[ex['id'], f"{flow_instance.CACHE_DIR}/{name}"]: self.uploader(w))
                item_layout.addWidget(upload_button)
                ##
                item_widget.setLayout(item_layout)
                #listitem widget
                list_item = QListWidgetItem(self.workout_list)
                list_item.setSizeHint(item_widget.sizeHint())
                list_item.setData(QtCore.Qt.UserRole, [ex['id'], f"{flow_instance.CACHE_DIR}/{name}"])
                self.workout_list.addItem(list_item)
                self.workout_list.setItemWidget(list_item, item_widget)

            self.workout_list.itemClicked.connect(self.handle_workout_click)
        return 0

    def handle_workout_click(self, item):
        workout_data = item.data(QtCore.Qt.UserRole)
        self.uploader(workout_data)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())
    def refresh_button(self):
        self.refresh.setText("Refreshing...")
        self.load_trainings()
        self.refresh.setText("")
        print('das')


    def uploader(self, workout_data:str):
        self.clearLayout(self.right_layout)


        #-------------------------------------------
        workout = None
        with open(workout_data[1]) as j:
            exercise_list = json.load(j)
            for i in exercise_list:
                if i['id'] == workout_data[0]:
                    workout = i

        # altitude data ----
        for i in workout['samples']:
            if i['sample_type'] == 3:
                data = i['data']
                altitudes = [float(i) for i in data.split(",")]

        months = {index + 1: month for index, month in
                  enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}

        year, month, day, hour = time_split(workout['start_time'])
        n_month = months[int(month)]
        activity_type = "futas" #-----------
        intensity = "3"
        total_time = ap_calc_duration(workout['duration'])
        distance = calc_distance(workout['distance'])
        climb = calc_altitude(altitudes)
        shoes = "Not Specified"
        avg_hr = workout['heart_rate']['average']
        max_hr = workout['heart_rate']['maximum']
        resting_hr = ""
        sleep = ""
        weight = ""

        #-------x---
        gridLayout_Top = QGridLayout()
        gridLayout_Top.setSpacing(10)

        # Row 0: Date and Session
        labelDate = QLabel("Date")
        self.comboBoxMonth = QComboBox()
        self.comboBoxMonth.addItems(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        self.comboBoxMonth.setEditable(True)
        self.comboBoxDay = QComboBox()
        self.comboBoxDay.addItems([f"{i:02d}" for i in range(1, 32)])
        self.comboBoxDay.setEditable(True)
        self.comboBoxYear = QComboBox()
        self.comboBoxYear.addItems(["2023", "2024", "2025", "2026"])
        self.comboBoxYear.setEditable(True)

        labelSession = QLabel("session:")
        self.comboBoxSession = QComboBox()
        self.comboBoxSession.addItems(
            ["--", "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
             "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM", "12 PM", ])
        self.comboBoxSession.setEditable(True)
        date_hbox = QHBoxLayout()
        date_hbox.setSpacing(2)
        date_hbox.addWidget(self.comboBoxMonth)
        date_hbox.addWidget(self.comboBoxDay)
        date_hbox.addWidget(self.comboBoxYear)
        date_hbox.addStretch(1)

        gridLayout_Top.addWidget(labelDate, 0, 0, Qt.AlignTop)
        gridLayout_Top.addLayout(date_hbox, 0, 1, 1, 1)
        gridLayout_Top.addWidget(labelSession, 0, 5)
        gridLayout_Top.addWidget(self.comboBoxSession, 0, 6)

        # Row 1: Activity and Workout
        labelActivity = QLabel("Activity / Sport")
        self.comboBoxActivity = QComboBox()
        self.comboBoxActivity.setEditable(True)
        self.comboBoxActivity.addItems(["futás", "Running", "Cycling", "Swimming"])

        labelWorkout = QLabel("Workout:")
        self.comboBoxWorkout = QComboBox()
        self.comboBoxWorkout.setEditable(True)
        self.comboBoxWorkout.addItems(
            ['"Training"', 'Race', 'Long', 'Intervals', 'Hills', 'Tempo', 'Warm up/down', '[None]'])
        gridLayout_Top.addWidget(labelActivity, 1, 0)
        gridLayout_Top.addWidget(self.comboBoxActivity, 1, 1, 1, 3)
        gridLayout_Top.addWidget(labelWorkout, 1, 5)
        gridLayout_Top.addWidget(self.comboBoxWorkout, 1, 6)

        # Row 2: Intensity
        labelIntensity = QLabel("Intensity:")
        self.comboBoxIntensity = QComboBox()
        self.comboBoxIntensity.addItems(["0", "1", "2", "3", "4", "5"])
        self.comboBoxIntensity.setEditable(True)
        self.comboBoxIntensity.setFixedWidth(60)
        labelIntensityHint = QLabel("(1-low, 5-high)")
        labelIntensityHint.setStyleSheet('''font-weight:200;''')

        intensity_hbox = QHBoxLayout()
        intensity_hbox.setSpacing(5)
        intensity_hbox.addWidget(self.comboBoxIntensity)
        intensity_hbox.addWidget(labelIntensityHint)
        intensity_hbox.addStretch(1)

        gridLayout_Top.addWidget(labelIntensity, 2, 0)
        gridLayout_Top.addLayout(intensity_hbox, 2, 1, 1, 3)

        gridLayout_Top.setColumnStretch(4, 1)

        self.right_layout.addLayout(gridLayout_Top)

        # --- Activity Sub-type ---
        subTypeHBox = QHBoxLayout()
        labelActivitySubType = QLabel("activity sub-type (or keywords):")
        self.lineEditActivitySubType = QLineEdit()
        subTypeHBox.addWidget(labelActivitySubType)
        subTypeHBox.addWidget(self.lineEditActivitySubType)
        self.right_layout.addLayout(subTypeHBox)

        # --- Time/Distance Grid ---
        gridLayout_TimeDist = QGridLayout()
        gridLayout_TimeDist.setSpacing(10)

        # Row 0: Total Time and Hint
        labelTotalTime = QLabel("Total time")
        self.lineEditTotalTime = QLineEdit()
        self.lineEditTotalTime.setFixedWidth(100)
        # Simple hint without rich text/color
        labelTimeHint = QLabel('HHMMSS or MMSS. e.g. "500" = 5 minutes.')
        labelTimeHint.setStyleSheet('''font-weight:100;''')
        labelTimeHint.setWordWrap(True)

        gridLayout_TimeDist.addWidget(labelTotalTime, 0, 0)
        gridLayout_TimeDist.addWidget(self.lineEditTotalTime, 0, 1)
        gridLayout_TimeDist.addWidget(labelTimeHint, 0, 2, 1, 5)

        # Row 1: Distance, Pace, Units, Climb
        labelDistance = QLabel("distance:")
        self.lineEditDistance = QLineEdit()
        self.lineEditDistance.setFixedWidth(100)
        labelUnits = QLabel("units:")
        self.comboBoxUnits = QComboBox()
        self.comboBoxUnits.addItems(["km", "mi"])
        self.comboBoxUnits.setEditable(True)
        labelClimb = QLabel("climb:")
        self.lineEditClimb = QLineEdit()
        self.lineEditClimb.setFixedWidth(80)
        labelClimbUnit = QLabel("m")

        gridLayout_TimeDist.addWidget(labelDistance, 1, 0)
        gridLayout_TimeDist.addWidget(self.lineEditDistance, 1, 1)
        gridLayout_TimeDist.addWidget(labelUnits, 1, 5)
        gridLayout_TimeDist.addWidget(self.comboBoxUnits, 1, 6)
        gridLayout_TimeDist.addWidget(labelClimb, 1, 8)
        gridLayout_TimeDist.addWidget(self.lineEditClimb, 1, 9)
        gridLayout_TimeDist.addWidget(labelClimbUnit, 1, 10)

        gridLayout_TimeDist.setColumnStretch(10, 1)

        self.right_layout.addLayout(gridLayout_TimeDist)

        # --- Shoes Section ---
        horizontalLayout_Shoes = QHBoxLayout()
        # Keep object name, but style targeting it is removed
        labelShoes = QLabel("Shoes")
        labelShoes.setObjectName("labelShoes")
        self.comboBoxShoes = QComboBox()
        self.comboBoxShoes.setEditable(True)
        self.comboBoxShoes.setMinimumWidth(150)
        self.comboBoxShoes.addItems(["Not Specified"])

        horizontalLayout_Shoes.addWidget(labelShoes)
        horizontalLayout_Shoes.addWidget(self.comboBoxShoes)
        horizontalLayout_Shoes.addStretch(1)

        self.right_layout.addLayout(horizontalLayout_Shoes)

        # --- Separator Line ---
        lineSeparatorMetrics = QFrame()
        lineSeparatorMetrics.setFrameShape(QFrame.HLine)
        lineSeparatorMetrics.setFrameShadow(QFrame.Sunken)  # Default sunken look
        self.right_layout.addWidget(lineSeparatorMetrics)

        # --- Metrics Grid ---
        gridLayout_Metrics = QGridLayout()
        gridLayout_Metrics.setSpacing(10)

        hr_vbox = QHBoxLayout()
        avg_hr_hbox = QHBoxLayout()
        avg_hr_hbox.addWidget(QLabel("Avg HR:"))
        self.lineEditAvgHR = QLineEdit()
        self.lineEditAvgHR.setFixedWidth(60)
        avg_hr_hbox.addWidget(self.lineEditAvgHR)
        avg_hr_hbox.addStretch(1)
        hr_vbox.addLayout(avg_hr_hbox)
        max_hr_hbox = QHBoxLayout()
        max_hr_hbox.addWidget(QLabel("Max HR:"))
        self.lineEditMaxHR = QLineEdit()
        self.lineEditMaxHR.setFixedWidth(60)
        max_hr_hbox.addWidget(self.lineEditMaxHR)
        max_hr_hbox.addStretch(1)
        hr_vbox.addLayout(max_hr_hbox)

        gridLayout_Metrics.addLayout(hr_vbox, 0, 0)

        labelRestingHR = QLabel("Resting-HR:")
        self.lineEditRestingHR = QLineEdit()
        self.lineEditRestingHR.setFixedWidth(60)
        labelSleep = QLabel("Sleep(hrs):")
        self.lineEditSleep = QLineEdit()
        self.lineEditSleep.setFixedWidth(60)
        labelWeight = QLabel("Weight(kg):")
        self.lineEditWeight = QLineEdit()
        self.lineEditWeight.setFixedWidth(60)

        injured_label = QLabel('Injured?')
        self.checkBoxInjured = QCheckBox()

        sick_label = QLabel('Sick?')
        self.checkBoxSick = QCheckBox()

        rest_label = QLabel('Rest day?')
        self.checkBoxRest = QCheckBox()


        # Using simple HBoxes for the second row of metrics for alignment
        resting_hr_hbox = QHBoxLayout()
        resting_hr_hbox.addWidget(labelRestingHR)
        resting_hr_hbox.addWidget(self.lineEditRestingHR)
        resting_hr_hbox.addStretch(1)

        sleep_hbox = QHBoxLayout()
        sleep_hbox.addWidget(labelSleep)
        sleep_hbox.addWidget(self.lineEditSleep)
        sleep_hbox.addStretch(1)

        injured_vbox = QVBoxLayout()
        injured_vbox.addWidget(injured_label)
        injured_vbox.addWidget(self.checkBoxInjured)

        sick_vbox = QVBoxLayout()
        sick_vbox.addWidget(sick_label)
        sick_vbox.addWidget(self.checkBoxSick)

        rest_vbox = QVBoxLayout()
        rest_vbox.addWidget(rest_label)
        rest_vbox.addWidget(self.checkBoxRest)


        weight_hbox = QHBoxLayout()
        weight_hbox.addWidget(labelWeight)
        weight_hbox.addWidget(self.lineEditWeight)
        weight_hbox.addStretch(1)

        gridLayout_Metrics.addLayout(resting_hr_hbox, 1, 0)
        gridLayout_Metrics.addLayout(sleep_hbox, 1, 1)
        gridLayout_Metrics.addLayout(weight_hbox, 1, 2)
        gridLayout_Metrics.addLayout(injured_vbox, 1, 3)
        gridLayout_Metrics.addLayout(sick_vbox,1,4)
        gridLayout_Metrics.addLayout(rest_vbox,1,5)

        gridLayout_Metrics.setColumnStretch(0, 1)
        gridLayout_Metrics.setColumnStretch(1, 1)
        gridLayout_Metrics.setColumnStretch(2, 1)
        gridLayout_Metrics.setColumnStretch(3, 1) # Remove last stretch?

        self.right_layout.addLayout(gridLayout_Metrics)

        # --- Description Section ---
        labelDescription = QLabel("Description")
        self.textEditDescription = QTextEdit()
        self.textEditDescription.setMinimumHeight(100)

        self.right_layout.addWidget(labelDescription)
        self.right_layout.addWidget(self.textEditDescription)

        # --- Bottom Submit Button ---
        horizontalLayout_BottomSubmit = QHBoxLayout()
        horizontalLayout_BottomSubmit.addStretch(1)
        self.pushButtonSubmitBottom = QPushButton("Submit")
        self.pushButtonSubmitBottom.setStyleSheet('''
            QPushButton {
                background-color: rgb(214, 143, 36);
                color: white;
                font-weight: bold;
                font-size: 17px;
                border: none;
                border-radius: 9px;
                padding: 4px 18px;
            }

            QPushButton:hover {
                background-color: #FF8C00;
            }

            QPushButton:pressed {
                background-color: #E67300;
            }
        ''')
        self.pushButtonSubmitBottom.clicked.connect(lambda: self.start_upload(activity_type))
        horizontalLayout_BottomSubmit.addWidget(self.pushButtonSubmitBottom)

        self.right_layout.addLayout(horizontalLayout_BottomSubmit)

        # --- Set Overall Stretch ---
        # Give the description text edit vertical stretch
        self.right_layout.setStretchFactor(self.textEditDescription, 1)

        self.lineEditActivitySubType.setAlignment(Qt.AlignCenter)
        self.lineEditTotalTime.setAlignment(Qt.AlignCenter)
        self.lineEditDistance.setAlignment(Qt.AlignCenter)
        self.lineEditClimb.setAlignment(Qt.AlignCenter)
        self.lineEditAvgHR.setAlignment(Qt.AlignCenter)
        self.lineEditMaxHR.setAlignment(Qt.AlignCenter)
        self.lineEditRestingHR.setAlignment(Qt.AlignCenter)
        self.lineEditSleep.setAlignment(Qt.AlignCenter)
        self.lineEditWeight.setAlignment(Qt.AlignCenter)



        # --- Set Initial Values ---
        self.comboBoxYear.setCurrentText(year)
        self.comboBoxMonth.setCurrentText(n_month)
        self.comboBoxDay.setCurrentText(day)
        self.comboBoxSession.setCurrentText(hour)
        self.comboBoxActivity.setCurrentText(activity_type)
        self.comboBoxIntensity.setCurrentText(intensity)
        self.lineEditTotalTime.setText(total_time)
        self.lineEditDistance.setText(distance)
        self.lineEditClimb.setText(climb)
        self.comboBoxShoes.setCurrentText(shoes)
        self.lineEditAvgHR.setText(str(avg_hr))
        self.lineEditMaxHR.setText(str(max_hr))
        self.lineEditRestingHR.setText(resting_hr)
        self.lineEditSleep.setText(sleep)
        self.lineEditWeight.setText(weight)

        # uploadddd

    def start_upload(self, task):
        # Create a worker instance
        self.worker = Uploading(self.comboBoxYear.currentText(),self.comboBoxMonth.currentText(),self.comboBoxDay.currentText(),self.comboBoxSession.currentText(),self.comboBoxActivity.currentText(),self.comboBoxWorkout.currentText(),self.comboBoxIntensity.currentText(), self.lineEditActivitySubType.text(),self.lineEditTotalTime.text(),self.lineEditDistance.text(),self.comboBoxUnits.currentText(),self.lineEditClimb.text(),self.comboBoxShoes.currentText(),self.lineEditAvgHR.text(),self.lineEditMaxHR.text(), self.lineEditRestingHR.text(),self.lineEditSleep.text(),self.lineEditWeight.text(), self.textEditDescription.toPlainText(),self.checkBoxInjured.checkState(), self.checkBoxSick.checkState(), self.checkBoxRest.checkState(), {})
        # Connect the finished signal to a callback
        self.worker.show_injury_window.connect(self.show_injury_window)  # Connect signal
        self.worker.finished.connect(self.upload_finished)
        # Start the worker
        self.worker.start()

    def finished(self):
        # Handle the result of the background task
        print(f"yaaay")
    def show_injury_window(self, year, month, day):
        self.injury_window = InjuryWindow(year, month, day, self .worker)
        self.injury_window.show()
        self.injury_window.raise_()
        self.injury_window.activateWindow()

    def upload_finished(self, result):
        print(result)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PolarAttack"))
        self.menu.setText(_translate("MainWindow", "..."))
        self.attckp.setText(_translate("MainWindow", "Attackpoint"))
        self.polarflow.setText(_translate("MainWindow", "PolarFlow"))
        self.name.setText(_translate(f"MainWindow",
                                     f"<html><head/><body><p><span style=\" font-weight:700; color:white;\">{load_yml(f"{Path.home()}/Library/Application Support/PolarAttack/config.yml")['name']}</span></p></body></html>"))



class LoadingWindow(QWidget):
    def __init__(self):
        super().__init__()


    def setupUI(self,w):
        w.setObjectName('w')
        w.resize(300,90)
        w.setStyleSheet("background-color: rgb(0,0,0);") #218	129	48
        w.setWindowFlags(Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(w)
        layout = QHBoxLayout(self.centralwidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.loadingLabel = QLabel("Loading",self.centralwidget)
        self.loadingLabel.setStyleSheet("color: rgb(218,129,48); font-size:36px; font-family:Arial;")
        layout.addWidget(self.loadingLabel)
        w.setCentralWidget(self.centralwidget)

        self.animation = QLabel(self.centralwidget)
        layout.addWidget(self.animation)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)
        # Load and set the logo image
        pixmap = QPixmap("ui/icons/logo.png")  # Path to the image
        scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale the image
        self.image_label.setPixmap(scaled_pixmap)


class InjuryWindow(QMainWindow):
    def __init__(self, year, month, day, uploading_worker):
        super().__init__()
        self.year = year
        self.month = month
        self.day = day
        self.center()
        self.setWindowTitle("Injury Report")
        self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: rgb(24,24,24);
                    color: white;
                    font-family: Arial;
                }
                QGroupBox {
                    background-color: rgb(30,30,30);
                    border: 2px solid rgb(77,77,77);
                    border-radius: 10px;
                    color: white;
                    font-weight: 700;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                }
                QComboBox, QLineEdit {
                    background-color: rgb(50, 50, 50);
                    color: white;
                    border: 1px solid rgb(77, 77, 77);
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QComboBox QAbstractItemView {
                    background-color: rgb(50, 50, 50);
                    color: white;
                    selection-background-color: orange;
                    selection-color: black;
                    border: none;
                }
                QTextEdit {
                    background-color: rgb(77, 77, 77);
                    color: white;
                    border: 1px solid rgb(50, 50, 50);
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QCheckBox {
                    color: white;
                    font-size: 14px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid rgb(77, 77, 77);
                    background-color: rgb(50, 50, 50);
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid orange;
                    background-color: orange;
                    border-radius: 3px;
                }
                QPushButton {
                    background-color: rgb(214, 143, 36);
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    border: none;
                    border-radius: 9px;
                    padding: 4px 18px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
                QPushButton:pressed {
                    background-color: #E67300;
                }
                QComboBox QAbstractItemView QScrollBar:vertical {
                    background: #444;
                    width: 12px;
                    margin: 0px 0px 0px 0px;
                }
                QComboBox QAbstractItemView QScrollBar::handle:vertical {
                    background: orange;
                    min-height: 20px;
                    border-radius: 6px;
                }
                QComboBox QAbstractItemView QScrollBar::add-line:vertical,
                QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                    background: none;
                    height: 0px;
                }
                QComboBox QAbstractItemView QScrollBar::up-arrow:vertical,
                QComboBox QAbstractItemView QScrollBar::down-arrow:vertical {
                    background: none;
                }
            """)
        self.init_ui()
        self.uploading_worker = uploading_worker

    def closeEvent(self, a0):
        self.uploading_worker.injury_no_thanks()
        a0.accept()


    def init_ui(self):
        central_widget = QWidget(self)
        main_layout = QHBoxLayout(central_widget)
        layout = QVBoxLayout()
        right = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(right)

        self.setCentralWidget(central_widget)

        #left side ------ - - - - - - --   - --  - - -
        # Injury Report Title
        title = QLabel("Injury Report")
        title.setFont(QFont("Arial",24, QFont.Bold))
        layout.addWidget(title)

        # Start Date
        start_date_layout = QHBoxLayout()
        self.yearCombo = QComboBox()
        self.yearCombo.addItems(["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"])
        self.yearCombo.setCurrentText(str(self.year))
        self.yearCombo.setEditable(True)

        self.monthsCombo = QComboBox()
        self.monthsCombo.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        self.monthsCombo.setCurrentText(str(self.month))
        self.monthsCombo.setEditable(True)

        self.dayCombo = QComboBox()
        self.dayCombo.addItems([f"{i:02d}" for i in range(1, 32)])
        self.dayCombo.setCurrentText(str(self.day))
        self.dayCombo.setEditable(True)


        start_date_label = QLabel("Start Date")
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(self.yearCombo)
        start_date_layout.addWidget(self.monthsCombo)
        start_date_layout.addWidget(self.dayCombo)
        layout.addLayout(start_date_layout)


        # Recovered Checkbox
        recovered_layout = QHBoxLayout()
        recovered_layout.addWidget(QLabel("Recovered?"))
        self.recoveredCheckbox = QCheckBox()
        recovered_layout.addWidget(self.recoveredCheckbox)
        self.recoveredCheckbox.stateChanged.connect(self.recovered_changed) ##############
        layout.addLayout(recovered_layout)

        # End Date
        self.end_date_layout = QHBoxLayout()

        self.end_date_layout = QHBoxLayout()
        self.end_year = QComboBox()
        self.end_year.addItems(["2023", "2024", "2025", "2026", "2027", "2028", "2029", "2030"])
        self.end_year.setCurrentText(str(self.year))
        self.end_year.setEditable(True)

        self.end_months = QComboBox()
        self.end_months.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        self.end_months.setCurrentText(str(self.month))
        self.end_months.setEditable(True)

        self.end_days = QComboBox()
        self.end_days.addItems([f"{i:02d}" for i in range(1, 32)])
        self.end_days.setCurrentText(str(self.day))
        self.end_days.setEditable(True)

        end_date_label = QLabel("End Date")

        self.end_date_layout.addWidget(end_date_label)
        self.end_date_layout.addWidget(self.end_year)
        self.end_date_layout.addWidget(self.end_months)
        self.end_date_layout.addWidget(self.end_days)
        layout.addLayout(self.end_date_layout)
        #aouto hide
        self.end_months.setVisible(False)
        self.end_year.setVisible(False)
        self.end_days.setVisible(False)

        # Type
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type"))
        self.typeCombo = QComboBox()
        self.typeCombo.setEditable(True)
        self.typeCombo.addItems(["Foot -- Ankle Sprain", "Foot -- Blisters", "Foot -- Bunions", "Foot -- Fracture", "Foot -- Impact wound / trauma", "Foot -- Morton's Neuroma", "Foot -- Other", "Foot -- Plantar Fasciitis", "Foot -- Stress Fracture", "Lower Leg -- Achilles Tendonitis", "Lower Leg -- Calf Strain", "Lower Leg -- Fracture", "Lower Leg -- Impact wound / trauma", "Lower Leg -- Other", "Lower Leg -- Shin Splints", "Lower Leg -- Stress Fracture", "Knee -- Fracture", "Knee -- Hyperextension", "Knee -- Iliotibial Band Syndrome", "Knee -- Impact wound / trauma", "Knee -- Ligament tear", "Knee -- Other", "Knee -- Patellar tendonitis", "Upper Leg -- Fracture", "Upper Leg -- Hamstring Pain", "Upper Leg -- Impact wound / trauma", "Upper Leg -- Other", "Upper Leg -- Stress Fracture", "Hip/Pelvis -- Fracture", "Hip/Pelvis -- Groin Pull", "Hip/Pelvis -- Hip Pain", "Hip/Pelvis -- Impact wound / trauma", "Hip/Pelvis -- Other", "Hip/Pelvis -- Piriformis", "Hip/Pelvis -- Sciatica", "Torso -- Fracture", "Torso -- Impact wound / trauma", "Torso -- Lower Back Pain", "Torso -- Other", "Torso -- Upper Back Pain", "Shoulder -- Impact wound / trauma", "Shoulder -- Other", "Shoulder -- Rotator Cuff injury", "Shoulder -- Shoulder Pain", "Arm -- Fracture", "Arm -- Impact wound / trauma", "Arm -- Other", "Head/Neck -- Concussion", "Head/Neck -- Fracture", "Head/Neck -- Impact wound / trauma", "Head/Neck -- Neck Pain", "Head/Neck -- Other", "Eye -- Foreign Body / Abrasion", "Other -- Dehydration", "Other -- Diarrhea", "Other -- Heat Exhaustion / Stroke", "Other -- Hyponatremia", "Other -- Hypothermia", "Other -- Other", "Sick -- Cold", "Sick -- COVID", "Sick -- Flu", "Sick -- Other"])
        type_layout.addWidget(self.typeCombo, alignment=Qt.AlignLeft)
        layout.addLayout(type_layout)

        # Side
        side_layout = QHBoxLayout()
        side_layout.addWidget(QLabel("Side"))
        self.sideCombo = QComboBox()
        self.sideCombo.addItems(["N/A", "L", "R"])
        self.sideCombo.setEditable(True)
        side_layout.addWidget(self.sideCombo)
        layout.addLayout(side_layout)

        # Grade
        grade_layout = QHBoxLayout()
        grade_layout.addWidget(QLabel("Grade"))
        self.gradeCombo = QComboBox()
        self.gradeCombo.addItems(["1", "2", "3", "4"])
        self.gradeCombo.setEditable(True)
        self.gradeCombo.setCurrentText("2")
        grade_layout.addWidget(self.gradeCombo)
        grade_layout.addWidget(QLabel("(peak severity)"))
        layout.addLayout(grade_layout)

        # Description
        layout.addWidget(QLabel("Description"))
        self.descriptonEdit = QTextEdit()
        layout.addWidget(self.descriptonEdit)


        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.start_injury_uploading)
        submit_button.setStyleSheet('''
                                       QPushButton {
                                            background-color: rgb(214, 143, 36);
                                            color: white;
                                            font-weight: bold;
                                            font-size: 17px;
                                            border: none;
                                            border-radius: 9px;
                                            padding: 4px 18px;
                                        }
                            
                                        QPushButton:hover {
                                            background-color: #FF8C00;
                                        }
                            
                                        QPushButton:pressed {
                                            background-color: #E67300;
                                        } 
                                    ''')
        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button, alignment=Qt.AlignLeft)
        layout.addLayout(button_layout)

        #right side  - - - - --  -- -------  - -- -  - - - - - -------- - --------------------- - - - --
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout)

        big_text = QGroupBox()
        right_layout.addWidget(big_text)
        blayout = QVBoxLayout(big_text)

        severity = QGroupBox()
        right_layout.addWidget(severity)
        slayout = QVBoxLayout(severity)

        #----------


        info = QLabel("You can use the form below to record more structured\ndetails about your injury or illness.\n"
                      "This makes it much easier to review or\nanalyze your injury history in the future.")
        thanks_btn = QPushButton("No thanks")
        thanks_btn.clicked.connect(self.no_thanks_btn)
        thanks_btn.setStyleSheet(''' QPushButton {
                                                    background-color: rgb(214, 143, 36);
                                                    color: white;
                                                    font-weight: bold;
                                                    font-size: 17px;
                                                    border: none;
                                                    border-radius: 9px;
                                                    padding: 4px 18px;
                                                }

                                                QPushButton:hover {
                                                    background-color: #FF8C00;
                                                }

                                                QPushButton:pressed {
                                                    background-color: #E67300;
                                                } 
                                            ''')
        blayout.addWidget(info)
        blayout.addWidget(thanks_btn)

        #----------
        discomfort_level = DiscomfortWidget()
        slayout.addWidget(discomfort_level)
        #table -----

    def center(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def recovered_changed(self, state):
        if state == Qt.Checked:
            self.end_months.setVisible(True)
            self.end_year.setVisible(True)
            self.end_days.setVisible(True)

        else:
            self.end_months.setVisible(False)
            self.end_year.setVisible(False)
            self.end_days.setVisible(False)

    def start_injury_uploading(self):
        # injury data
        self.i_data = {
            "no": False,
            "year": self.yearCombo.currentText(),
            "month": self.monthsCombo.currentText(),
            "day": self.dayCombo.currentText(),
            "recovered": self.recoveredCheckbox.isChecked(),
            "end_year": self.end_year.currentText(),
            "end_month": self.end_months.currentText(),
            "end_day": self.end_days.currentText(),
            "type": self.typeCombo.currentText(),
            "side": self.sideCombo.currentText(),
            "grade": self.gradeCombo.currentText(),
            "description": self.descriptonEdit.toPlainText()
        }
        self.close()
        self.uploading_worker.injury_upload(self.i_data)
    def no_thanks_btn(self):
        self.close()
        self.uploading_worker.injury_no_thanks()

class DiscomfortWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the discomfort level display"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        main_layout.setSpacing(0)  # Remove spacing between rows

        # Create header
        self.create_header(main_layout)

        # Create discomfort level entries
        self.create_discomfort_levels(main_layout)

        # Apply styling
        self.apply_styling()

    def create_header(self, layout):
        """Create the header row"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(4, 4, 4, 4)
        header_layout.setSpacing(0)

        # Header labels
        level_header = QLabel("#")
        level_header.setFont(QFont("Arial", 16, QFont.Bold))
        level_header.setAlignment(Qt.AlignLeft)

        discomfort_header = QLabel("Discomfort Level")
        discomfort_header.setFont(QFont("Arial", 12, QFont.Bold))
        #discomfort_header.setAlignment(Qt.AlignCenter)

        impact_header = QLabel("Impact on\nCompetitive Level")
        impact_header.setFont(QFont("Arial", 12, QFont.Bold))
        #impact_header.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(level_header)
        header_layout.addWidget(discomfort_header)
        header_layout.addWidget(impact_header)

        layout.addWidget(header_frame)

    def create_discomfort_levels(self, layout):
        """Create individual discomfort level entries"""
        data = [
            {
                "level": "1",
                "discomfort": "discomfort during exercise\nwith relief possible;\nmay occur only during hard exertion",
                "impact": "none or slight"
            },
            {
                "level": "2",
                "discomfort": "increasingly painful during exercise;\nmay persist at rest",
                "impact": "decreased ability to compete"
            },
            {
                "level": "3",
                "discomfort": "significant discomfort;\nunable to exercise",
                "impact": "unable to exercise and\ncannot compete"
            },
            {
                "level": "4",
                "discomfort": "discomfort may be severe",
                "impact": "out for season"
            }
        ]

        for entry in data:
            self.create_level_row(layout, entry)

    def create_level_row(self, layout, data):
        """Create a single discomfort level row"""
        row_frame = QFrame()
        row_frame.setFrameStyle(QFrame.Box)
        row_layout = QHBoxLayout(row_frame)
        row_layout.setContentsMargins(4, 3, 4, 3)
        row_layout.setSpacing(0)

        # Level number
        level_label = QLabel(data["level"])
        level_label.setFont(QFont("Arial", 10, QFont.Bold))
        level_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Discomfort description
        discomfort_label = QLabel(data["discomfort"])
        discomfort_label.setFont(QFont("Arial", 10, QFont.Bold))
        discomfort_label.setWordWrap(True)
        discomfort_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Impact description
        impact_label = QLabel(data["impact"])
        impact_label.setFont(QFont("Arial", 10, QFont.Bold))
        impact_label.setWordWrap(True)
        impact_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Add to layout
        row_layout.addWidget(level_label)
        row_layout.addWidget(discomfort_label)
        row_layout.addWidget(impact_label)

        layout.addWidget(row_frame)

    def apply_styling(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            QFrame {
                background-color: #404040;
                border: 1px solid #666666;
                margin: 0px;
            }
            QLabel {
                color: white;
                padding: 2px;
                background-color: transparent;
                border: none;
            }
        """)

class NewShoeOrSport(QDialog):
    def __init__(self, type_:str, no:str, data:list):
        super().__init__()
        self.type = type_
        self.no = no
        self.data = data
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(f"Manage {self.type}")
        self.setModal(False)
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.resize(400, 400)
        self.setFixedSize(400, 400)
        #stylesheet
        self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: rgb(24,24,24);
                    color: white;
                    font-family: Arial;
                }
                QGroupBox {
                    background-color: rgb(30,30,30);
                    border: 2px solid rgb(77,77,77);
                    border-radius: 10px;
                    color: white;
                    font-weight: 700;
                }
                QLabel {
                    color: white;
                    font-size: 14px;
                }
                QComboBox, QLineEdit {
                    background-color: rgb(50, 50, 50);
                    color: white;
                    border: 1px solid rgb(77, 77, 77);
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QComboBox QAbstractItemView {
                    background-color: rgb(50, 50, 50);
                    color: white;
                    selection-background-color: orange;
                    selection-color: black;
                    border: none;
                }
                QTextEdit {
                    background-color: rgb(77, 77, 77);
                    color: white;
                    border: 1px solid rgb(50, 50, 50);
                    border-radius: 5px;
                    padding: 5px;
                    font-size: 14px;
                }
                QCheckBox {
                    color: white;
                    font-size: 14px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
                QCheckBox::indicator:unchecked {
                    border: 2px solid rgb(77, 77, 77);
                    background-color: rgb(50, 50, 50);
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    border: 2px solid orange;
                    background-color: orange;
                    border-radius: 3px;
                }
                QPushButton {
                    background-color: rgb(214, 143, 36);
                    color: white;
                    font-weight: bold;
                    font-size: 17px;
                    border: none;
                    border-radius: 9px;
                    padding: 4px 18px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                }
                QPushButton:pressed {
                    background-color: #E67300;
                }
                QComboBox QAbstractItemView QScrollBar:vertical {
                    background: #444;
                    width: 12px;
                    margin: 0px 0px 0px 0px;
                }
                QComboBox QAbstractItemView QScrollBar::handle:vertical {
                    background: orange;
                    min-height: 20px;
                    border-radius: 6px;
                }
                QComboBox QAbstractItemView QScrollBar::add-line:vertical,
                QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                    background: none;
                    height: 0px;
                }
                QComboBox QAbstractItemView QScrollBar::up-arrow:vertical,
                QComboBox QAbstractItemView QScrollBar::down-arrow:vertical {
                    background: none;
                }
            """)
        #center
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        #main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignTop)
        self.title_label.setStyleSheet("font-size: 24px;white-space: pre-line;")
        self.title_label.setWordWrap(True)
        self.title_label.setMinimumWidth(300)
        #layouts
        self.title_layout = QHBoxLayout()
        self. main_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignBottom)
        self.layout.addLayout(self.title_layout)
        self.layout.addLayout(self.main_layout)
        self.layout.addLayout(self.button_layout)

        self.title_layout.addWidget(self.title_label)

        #buttons
        self.cancel_btn = QPushButton()
        self.cancel_btn.setStyleSheet("""
                                       QPushButton {
                                            background-color: #53575e;
                                            color: white;
                                            font-weight: bold;
                                            font-size: 15px;
                                            border: none;
                                            border-radius: 9px;
                                            padding: 4px 18px;
                                        }
                                        QPushButton:hover {
                                            background-color: #777c85;
                                        }
                                        QPushButton:pressed {
                                            background-color: #bcc4d1;
                                        }
                                        """)
        self.cancel_btn.clicked.connect(self.cancel_clicked)

        self.ok_btn = QPushButton()
        self.button_layout.addWidget(self.cancel_btn)
        self.button_layout.addWidget(self.ok_btn)

        self.image_label = QLabel()
        self.list_groupbox = QGroupBox()
        self.group_layout = QVBoxLayout()

        #######
        if self.type == "shoes":
            self.image = QPixmap("ui/icons/shoe.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(self.image)
            self.main_layout.addWidget(self.image_label)

            self.main_layout.addWidget(self.list_groupbox)
            #button connect
            self.ok_btn.clicked.connect(lambda checked, x=self.no: self.manage_shoes(x))

            if self.no == "new":
                self.title_label.setText(f"{len(self.data)} új cipő található az <span style='color:orange;'>Attack</span>pointon!")


                for shoe in self.data:
                    shoe_label = QLabel(f"{shoe}")
                    shoe_label.setStyleSheet("background-color:None; font-weight: 700;color: orange")
                    self.group_layout.addWidget(shoe_label)
                self.list_groupbox.setLayout(self.group_layout)
                self.cancel_btn.setText("Nem adom hozzá")
                self.ok_btn.setText("Hozzáadom")

            else: #old
                self.title_label.setText(f"{len(self.data)} cipőt eltávolítottak az <span style='color:orange;'>Attack</span>pointról!<br>Itt is eltávolítod?")
                for shoe in self.data:
                    shoe_label = QLabel(f"{shoe}")
                    shoe_label.setStyleSheet("background-color:None; font-weight: 700;color: red")
                    self.group_layout.addWidget(shoe_label)
                self.list_groupbox.setLayout(self.group_layout)
                self.cancel_btn.setText("Meghagyom")
                self.ok_btn.setText("Eltávolítom")


        #######
        else:
            self.setModal(True) # can't itneract with other winodws
            self.image = QPixmap("ui/icons/running.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(self.image)
            self.main_layout.addWidget(self.image_label)

            self.main_layout.addWidget(self.list_groupbox)
            # button connect
            self.ok_btn.clicked.connect(lambda checked, x=self.no: self.manage_sports(x))

            if self.no == "new":
                self.title_label.setText(f"{len(self.data)} új sport  található az <span style='color:orange;'>Attack</span>pointon!")
                for sport in self.data:
                    sport_label = QLabel(f"{sport}")
                    sport_label.setStyleSheet("background-color:None; font-weight: 700;color: orange")
                    self.group_layout.addWidget(sport_label)
                self.list_groupbox.setLayout(self.group_layout)
                self.cancel_btn.setText("Nem adom hozzá")
                self.ok_btn.setText("Hozzáadom")
            else:
                self.title_label.setText(f"{len(self.data)} sportot eltávolítottak az <span style='color:orange;'>Attack</span>pointról!<br>Itt is eltávolítod?")
                for sport in self.data:
                    sport_label = QLabel(f"{sport}")
                    sport_label.setStyleSheet("background-color:None; font-weight: 700;color: red")
                    self.group_layout.addWidget(sport_label)
                self.list_groupbox.setLayout(self.group_layout)
                self.cancel_btn.setText("Meghagyom")
                self.ok_btn.setText("Eltávolítom")




    def cancel_clicked(self):
        self.close()
    def manage_shoes(self, no):
        pass
    def manage_sports(self, no):
        pass

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = InjuryWindow(2024,'May','04')
#     window.resize(500, 600)
#     window.show()
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication([])
    dialog =NewShoeOrSport("sports", "old", ['foci', 'futás'])
    dialog.exec_()