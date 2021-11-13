# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_Settings(object):
    def setupUi(self, MainWindow_Settings):
        MainWindow_Settings.setObjectName("MainWindow_Settings")
        MainWindow_Settings.resize(1063, 685)
        MainWindow_Settings.setStyleSheet("background-color: rgb(149, 181, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow_Settings)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1101, 701))
        self.label.setText("")
        self.label.setObjectName("label")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        self.back_btn.setGeometry(QtCore.QRect(60, 50, 191, 111))
        self.back_btn.setText("")
        self.back_btn.setObjectName("back_btn")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(120, 190, 821, 331))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.language_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(36)
        self.language_label.setFont(font)
        self.language_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.language_label.setObjectName("language_label")
        self.gridLayout.addWidget(self.language_label, 1, 0, 1, 1)
        self.back_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_comboBox.sizePolicy().hasHeightForWidth())
        self.back_comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.back_comboBox.setFont(font)
        self.back_comboBox.setStyleSheet("border: 2px solid grey;\n"
                                         "background-color: rgb(87, 96, 134);\n"
                                         "color:  rgb(255, 255, 255);\n"
                                         "font-weight: bold;\n"
                                         "padding: 5px;")
        self.back_comboBox.setObjectName("back_comboBox")
        self.gridLayout.addWidget(self.back_comboBox, 2, 1, 1, 1)
        self.speed_spin_box = QtWidgets.QSpinBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed_spin_box.sizePolicy().hasHeightForWidth())
        self.speed_spin_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.speed_spin_box.setFont(font)
        self.speed_spin_box.setStyleSheet("border: 2px solid grey;\n"
                                          "background-color:   rgb(87, 96, 134);\n"
                                          "padding: 5px;\n"
                                          "color: white;\n"
                                          "font-weight: bold;\n"
                                          "")
        self.speed_spin_box.setMinimum(1)
        self.speed_spin_box.setMaximum(10)
        self.speed_spin_box.setProperty("value", 3)
        self.speed_spin_box.setObjectName("speed_spin_box")
        self.gridLayout.addWidget(self.speed_spin_box, 0, 1, 1, 1)
        self.back_move_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(24)
        self.back_move_label.setFont(font)
        self.back_move_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.back_move_label.setObjectName("back_move_label")
        self.gridLayout.addWidget(self.back_move_label, 2, 0, 1, 1)
        self.speed_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(36)
        self.speed_label.setFont(font)
        self.speed_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.speed_label.setObjectName("speed_label")
        self.gridLayout.addWidget(self.speed_label, 0, 0, 1, 1)
        self.language_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_comboBox.sizePolicy().hasHeightForWidth())
        self.language_comboBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.language_comboBox.setFont(font)
        self.language_comboBox.setStyleSheet("border: 2px solid grey;\n"
                                             "background-color: rgb(87, 96, 134);\n"
                                             "color:  rgb(255, 255, 255);\n"
                                             "font-weight: bold;\n"
                                             "padding: 5px;")
        self.language_comboBox.setObjectName("language_comboBox")
        self.gridLayout.addWidget(self.language_comboBox, 1, 1, 1, 1)
        self.settings_label = QtWidgets.QLabel(self.centralwidget)
        self.settings_label.setGeometry(QtCore.QRect(310, 40, 481, 121))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(36)
        self.settings_label.setFont(font)
        self.settings_label.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_label.setObjectName("settings_label")
        self.cheat_button = QtWidgets.QPushButton(self.centralwidget)
        self.cheat_button.setGeometry(QtCore.QRect(960, 10, 91, 101))
        self.cheat_button.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.cheat_button.setStyleSheet("border: none;")
        self.cheat_button.setText("")
        self.cheat_button.setObjectName("cheat_button")
        MainWindow_Settings.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow_Settings)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_Settings)

    def retranslateUi(self, MainWindow_Settings):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_Settings.setWindowTitle(_translate("MainWindow_Settings", "MainWindow"))
        self.language_label.setText(_translate("MainWindow_Settings", "Language"))
        self.back_move_label.setText(_translate("MainWindow_Settings", "Backtrack animation"))
        self.speed_label.setText(_translate("MainWindow_Settings", "Speed"))
        self.settings_label.setText(_translate("MainWindow_Settings", "Settings"))
