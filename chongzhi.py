# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '充值.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
import json
import webbrowser

import requests
from PyQt5 import QtCore, QtWidgets
import sys

from PyQt5.QtWidgets import QMessageBox

server_base_url = "http://101.132.109.187:8000"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 277)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
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
        self.lineEditCardNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditCardNumber.setObjectName("lineEditCardNumber")
        self.horizontalLayout_2.addWidget(self.lineEditCardNumber)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEditPassword = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.horizontalLayout_3.addWidget(self.lineEditPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButtonRecharge = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRecharge.setObjectName("pushButtonRecharge")
        self.horizontalLayout_4.addWidget(self.pushButtonRecharge)
        self.pushButtonBuy = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBuy.setObjectName("pushButtonBuy")
        self.horizontalLayout_4.addWidget(self.pushButtonBuy)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 460, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "充值"))
        self.label.setText(_translate("MainWindow", "用户名"))
        self.label_2.setText(_translate("MainWindow", "卡号"))
        self.label_3.setText(_translate("MainWindow", "密码"))
        self.pushButtonRecharge.setText(_translate("MainWindow", "充值"))
        self.pushButtonBuy.setText(_translate("MainWindow", "购买卡密"))

class rechargeWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initListener()

    def initListener(self):
        self.ui.pushButtonBuy.clicked.connect(self.buy)
        self.ui.pushButtonRecharge.clicked.connect(self.recharge)

        # 卡密购买
    def buy(self):
        webbrowser.open(
            'https://w.url.cn/s/ArrIipN')

    def recharge(self):
        username = self.ui.lineEditUsername.text()
        card_number = self.ui.lineEditCardNumber.text()
        password = self.ui.lineEditPassword.text()
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = rechargeWindow()
    window.show()

    sys.exit(app.exec_())