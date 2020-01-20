# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
import requests
import sys
import re
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(348, 249)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEditName = QtWidgets.QLineEdit(Form)
        self.lineEditName.setObjectName("lineEditName")
        self.horizontalLayout_2.addWidget(self.lineEditName)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEditIdCard = QtWidgets.QLineEdit(Form)
        self.lineEditIdCard.setObjectName("lineEditIdCard")
        self.horizontalLayout_3.addWidget(self.lineEditIdCard)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEditContactPhone = QtWidgets.QLineEdit(Form)
        self.lineEditContactPhone.setObjectName("lineEditContactPhone")
        self.horizontalLayout_4.addWidget(self.lineEditContactPhone)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxProvince = QtWidgets.QComboBox(Form)
        self.comboBoxProvince.setObjectName("comboBoxProvince")
        self.horizontalLayout.addWidget(self.comboBoxProvince)
        self.comboBoxCity = QtWidgets.QComboBox(Form)
        self.comboBoxCity.setObjectName("comboBoxCity")
        self.horizontalLayout.addWidget(self.comboBoxCity)
        self.comboBoxCounty = QtWidgets.QComboBox(Form)
        self.comboBoxCounty.setObjectName("comboBoxCounty")
        self.horizontalLayout.addWidget(self.comboBoxCounty)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.lineEditLocation = QtWidgets.QLineEdit(Form)
        self.lineEditLocation.setText("街道/镇+村/小区/写字楼+门牌号")
        self.lineEditLocation.setObjectName("lineEditLocation")
        self.gridLayout.addWidget(self.lineEditLocation, 4, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "姓名    "))
        self.label_2.setText(_translate("Form", "身份证  "))
        self.label_3.setText(_translate("Form", "联系电话"))


class OrderInfoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initData()     # 初始化数据

    def initData(self):
        url = "https://res.mall.10010.cn/mall/front/js/areaInfo.js"

        res = requests.get(url)
        json_dict = eval(re.search("[{].*[}]", res.text).group())
        for province_item in json_dict['PROVINCE_LIST']:
            province_name = province_item['PROVINCE_NAME']
            self.ui.comboBoxProvince.addItem(province_name)
        # print(json_dict['PROVINCE_MAP'])



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = OrderInfoWidget()
    main.showMaximized()

    sys.exit(app.exec_())