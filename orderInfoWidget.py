# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
import requests
import sys
import webbrowser
import re
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json


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
        self.lineEditName = QtWidgets.QLineEdit(Form)                                 #####
        self.lineEditName.setObjectName("lineEditName")
        self.horizontalLayout_2.addWidget(self.lineEditName)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEditIdCard = QtWidgets.QLineEdit(Form)                             #####
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
        self.lineEditLocation.setText("街道/镇+村/小区/写字楼+门牌号")     #####
        self.lineEditLocation.setObjectName("lineEditLocation")
        self.gridLayout.addWidget(self.lineEditLocation, 4, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout)

        v_layout = QVBoxLayout()
        self.buttonUpdate = QPushButton("保存下单信息到服务器")
        self.buttonQueryOrder = QPushButton("订单查询")
        v_layout.addWidget(self.buttonUpdate)
        v_layout.addWidget(self.buttonQueryOrder)
        self.horizontalLayout_5.addLayout(v_layout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "姓名    "))
        self.label_2.setText(_translate("Form", "身份证  "))
        self.label_3.setText(_translate("Form", "联系电话"))


class OrderInfoWidget(QWidget):
    province_name = None
    province_code = None
    city_name = None
    city_code = None
    county_name = None
    county_code = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initData()     # 初始化数据
        self.initListener()     # 初始化监听器

    # 设置地址信息
    def initData(self):
        if not os.path.exists("areaInfo.json"):
            url = "https://res.mall.10010.cn/mall/front/js/areaInfo.js"
            res = requests.get(url)
            self.json_dict = eval(re.search("[{].*[}]", res.text).group())
            with open("areaInfo.json", 'w') as f:
                json.dump(self.json_dict, f)
        else:
            with open("areaInfo.json", 'r') as f:
                self.json_dict = json.load(f)

        for province_item in self.json_dict['PROVINCE_LIST']:
            province_name = province_item['PROVINCE_NAME']
            self.ui.comboBoxProvince.addItem(province_name)


        # 设置一些初始化数据
        self.ui.lineEditContactPhone.setText("")
        self.ui.lineEditName.setText("")
        self.ui.lineEditIdCard.setText("")
        self.ui.lineEditLocation.setText("街道/镇+村/小区/写字楼+门牌号")
        # 这个一定要写, 初始化combobox
        self.update_city_list_combobox("北京")

    def initListener(self):
        self.ui.buttonUpdate.clicked.connect(self.updateOrderInfo)
        self.ui.comboBoxProvince.activated[str].connect(self.update_city_list_combobox)
        self.ui.comboBoxCity.activated[str].connect(self.update_county_list_combobox)
        self.ui.comboBoxCounty.activated[str].connect(self.update_county_name_and_code)
        self.ui.buttonQueryOrder.clicked.connect(self.openBrowser)

    def openBrowser(self):
        webbrowser.open('https://m.10010.com/mfront/views/my-order/main.html#/orderlist?oneKey=t&refresh_sign=1&from=tx&openid=oMwiavzk1GcFKGKTK9QgVd5PUWMM')

    def update_city_list_combobox(self, province_name):
        # 先把这个省份的PROVINCE_CODE查出来
        self.province_name = province_name

        for province_item in self.json_dict['PROVINCE_LIST']:
            if province_item['PROVINCE_NAME'] == province_name:
                # 获得了
                self.province_code = province_item['PROVINCE_CODE']
                self.ui.comboBoxCity.clear()
                for city_item in self.json_dict['PROVINCE_MAP'][self.province_code]:
                    self.ui.comboBoxCity.addItem(city_item['CITY_NAME'])
                break

        self.update_county_list_combobox(self.ui.comboBoxCity.currentText())

    def update_county_list_combobox(self, city_name):
        self.city_name = city_name
        # 先把当前城市的城市代码查出来
        for city_item in self.json_dict['PROVINCE_MAP'][self.province_code]:
            if city_item['CITY_NAME'] == self.city_name:
                self.city_code = city_item['CITY_CODE']
                break

        self.ui.comboBoxCounty.clear()
        for county_item in self.json_dict['CITY_MAP'][self.city_code]:
            self.ui.comboBoxCounty.addItem(county_item['DISTRICT_NAME'])

        self.update_county_name_and_code(self.ui.comboBoxCounty.currentText())

    def update_county_name_and_code(self, count_name):
        for county_item in self.json_dict['CITY_MAP'][self.city_code]:
            if county_item['DISTRICT_NAME'] == count_name:
                self.county_code = county_item['DISTRICT_CODE']
                self.county_name = count_name
                break

        print(self.province_name, self.city_name, self.county_name, self.province_code, self.city_code, self.county_code)


    def updateOrderInfo(self):
        name = self.ui.lineEditName.text()
        id_card = self.ui.lineEditIdCard.text()
        contact_phone = self.ui.lineEditContactPhone.text()
        location = self.ui.lineEditLocation.text()

        QMessageBox.information(self, "提示", f"{name}\n{id_card}\n{contact_phone}\n"
                                            f"{self.province_name}\n{self.city_name}\n{self.county_name}\n{location}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = OrderInfoWidget()
    main.showMaximized()

    sys.exit(app.exec_())