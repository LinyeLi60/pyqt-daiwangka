"""
直接输入号码进行下单
"""
import json
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit, QPushButton, QApplication, QMessageBox


class DirectlyBuyWidget(QWidget):

    buyNumberSender = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.initData()
        self.initListener()


    def initUI(self):

        layout = QHBoxLayout()
        self.province_list_combobox = QComboBox()
        self.city_list_combobox = QComboBox()
        self.number_line_edit = QLineEdit("填下单号码")
        self.pushButton = QPushButton("点击下单")
        layout.addWidget(self.province_list_combobox)
        layout.addWidget(self.city_list_combobox)
        layout.addWidget(self.number_line_edit)
        layout.addWidget(self.pushButton)
        self.setLayout(layout)


    def initData(self):
        # 保存信息
        with open("area_code.json", 'r') as f:
            total_dict = json.load(f)
            self.provinceCodeToName = total_dict['provinceCodeToName']
            self.provinceNameToCode = total_dict['provinceNameToCode']
            self.cityNameToCode = total_dict['cityNameToCode']
            self.cityCodeToName = total_dict['cityCodeToName']
            self.provinceNameToCityNameList = total_dict['provinceNameToCityNameList']

    def initListener(self):
        self.province_list_combobox.addItems(self.provinceNameToCityNameList.keys())
        self.province_list_combobox.activated[str].connect(self.update_city_list_combobox)
        self.update_city_list_combobox(self.province_list_combobox.currentText())

        self.pushButton.clicked.connect(self.buy)

    def update_city_list_combobox(self, province_name):
        self.city_list_combobox.clear()
        self.city_list_combobox.addItems(self.provinceNameToCityNameList[province_name])

    def buy(self):
        province = self.province_list_combobox.currentText()
        city = self.city_list_combobox.currentText()
        number = self.number_line_edit.text().strip()
        if number == "" or number == "填下单号码" or number.__len__() != 11:
            QMessageBox.information(self, "提示", "请先填写号码")
        else:
            self.buyNumberSender.emit(number, province, city)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = DirectlyBuyWidget()
    main.show()

    sys.exit(app.exec_())