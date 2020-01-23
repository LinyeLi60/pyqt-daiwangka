# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import webbrowser
from PyQt5.QtWidgets import *
import requests
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json
from mainWindow import MainGUI
import uuid


server_base_url = "http://101.132.109.187:8000"
# server_base_url = "http://127.0.0.1:8000"


class RechargeWindow(QMainWindow):
    def __init__(self):
        super(RechargeWindow, self).__init__()
        self.initUI()
        self.initListener()

    def initUI(self):
        v_layout = QVBoxLayout()
        self.lineEditUsername = QLineEdit()
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(QLabel("用户名:"))
        h_layout_1.addWidget(self.lineEditUsername)

        self.lineEditCardNumber = QLineEdit()
        h_layout_2 = QHBoxLayout()
        h_layout_2.addWidget(QLabel("卡号:"))
        h_layout_2.addWidget(self.lineEditCardNumber)

        self.lineEditPassword = QLineEdit()
        h_layout_3 = QHBoxLayout()
        h_layout_3.addWidget(QLabel("卡密:"))
        h_layout_3.addWidget(self.lineEditPassword)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)
        self.button = QPushButton("充值按钮")
        v_layout.addWidget(self.button)
        # 用一个widget来套布局
        mainFrame = QWidget()
        mainFrame.setLayout(v_layout)
        self.setCentralWidget(mainFrame)

    def initListener(self):
        self.button.clicked.connect(self.recharge)

    def recharge(self):
        username = self.lineEditUsername.text().strip()
        card_number = self.lineEditCardNumber.text().strip()
        password = self.lineEditPassword.text().strip()
        if username == "":
            QMessageBox.information(self, "提示", "用户名为空")
        elif card_number == "":
            QMessageBox.information(self, "提示", "卡号为空")
        elif password == "":
            QMessageBox.information(self, "提示", "卡密为空")
        else:
            try:
                recharge_url = f"{server_base_url}/user/recharge"
                res = requests.post(recharge_url, data={'username': username,
                                                        'card_number': card_number, 'password': password})
                QMessageBox.information(self, "提示", json.loads(res.text)['desc'])
            except Exception as e:
                QMessageBox.information(self, "提示", "连接不上服务器")


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(469, 385)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditUsername = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditUsername.setObjectName("lineEditUsername")
        self.horizontalLayout.addWidget(self.lineEditUsername)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.horizontalLayout_2.addWidget(self.lineEditPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButtonRegister = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRegister.setObjectName("pushButtonRegister")
        self.horizontalLayout_3.addWidget(self.pushButtonRegister)
        self.pushButtonLogin = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.horizontalLayout_3.addWidget(self.pushButtonLogin)
        self.pushButtonExperience = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExperience.setObjectName("pushButtonExperience")
        self.horizontalLayout_3.addWidget(self.pushButtonExperience)
        self.pushButtonCopyUUID = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonCopyUUID.setObjectName("pushButtonCopyUUID")
        self.horizontalLayout_3.addWidget(self.pushButtonCopyUUID)

        # self.pushButtonBuy = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButtonBuy.setObjectName("pushButtonBuy")
        # self.horizontalLayout_3.addWidget(self.pushButtonBuy)

        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 469, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "登录"))
        self.label.setText(_translate("MainWindow", "用户名:"))
        self.label_2.setText(_translate("MainWindow", "密码:  "))
        self.pushButtonRegister.setText(_translate("MainWindow", "注册/注册信息也填上面两个空"))
        self.pushButtonLogin.setText(_translate("MainWindow", "登录"))
        self.pushButtonExperience.setText(_translate("MainWindow", "体验版"))
        self.pushButtonCopyUUID.setText(_translate("MainWindow", "复制uuid"))
        # self.pushButtonBuy.setText(_translate("MainWindow", "卡密购买"))


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.uuid = str(uuid.UUID(int=uuid.getnode()).int)      # 设备码

        # self.initData()     # 初始化数据
        self.initListener()     # 初始化监听器

    def initListener(self):
        self.ui.pushButtonLogin.clicked.connect(self.login)
        self.ui.pushButtonRegister.clicked.connect(self.register)
        self.ui.pushButtonExperience.clicked.connect(self.experience)     # 体验
        self.ui.pushButtonCopyUUID.clicked.connect(self.copyUUID)
        # self.ui.pushButtonRecharge.clicked.connect(self.recharge)

    def copyUUID(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.uuid)
        QMessageBox.information(self, "提示", f"uuid:{self.uuid}\n复制成功,如需更换设备请把uuid发给软件卖家")

    def recharge(self):
        self.recharge_window = RechargeWindow()
        self.recharge_window.show()

    # 卡密购买
    def buy(self):
        webbrowser.open(
            'https://w.url.cn/s/ArrIipN')

    def experience(self):
        self.main = MainGUI()
        self.main.setExperience()
        self.main.show()
        self.close()

    def register(self):
        username = self.ui.lineEditUsername.text().strip()
        password = self.ui.lineEditPassword.text().strip()
        if username == "":
            QMessageBox.information(self, "提示", "用户名为空")
        elif password == "":
            QMessageBox.information(self, "提示", "密码为空")
        else:
            try:
                url = f"{server_base_url}/user/register"
                res = requests.post(url, data={'username': username, 'password': password}, timeout=1)
                json_dict = json.loads(res.text)
                QMessageBox.information(self, "提示", json_dict['desc'])

            except Exception as e:
                QMessageBox.information(self, "错误", "无法连接上服务器,请重试")

    def login(self):
        username = self.ui.lineEditUsername.text().strip()
        password = self.ui.lineEditPassword.text().strip()

        if username == "":
            QMessageBox.information(self, "提示", "用户名为空")
        elif password == "":
            QMessageBox.information(self, "提示", "密码为空")

        # 尝试进行登录
        else:
            try:
                login_url = f"{server_base_url}/user/login"
                res = requests.post(login_url, data={'username': username, 'password': password, 'uuid': self.uuid},
                                    timeout=2)
                json_dict = json.loads(res.text)

                login_success = False
                if json_dict['ret'] == 0:
                    # 登录成功了
                    login_success = True
                QMessageBox.information(self, "提示", json_dict['desc'])
                if login_success:
                    self.close()
                    self.main = MainGUI()
                    self.main.show()

            except Exception as e:
                QMessageBox.information(self, "错误", "无法连接上服务器,请重试")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    loginWindow = LoginWindow()
    loginWindow.show()

    sys.exit(app.exec_())