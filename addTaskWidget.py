from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import requests
import json
import os
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Thread

# 添加任务的widget
class AddTaskWidget(QWidget):
    add_task_signal = pyqtSignal(dict)  # 把任务发出去
    logging_signal = pyqtSignal(str)  # 用来发日志的信号
    provinceCodeToName = {}
    provinceNameToCode = {}
    cityNameToCode = {}
    cityCodeToName = {}
    provinceNameToCityNameList = {}  # key: 省份名 value: 这个省下面所有市的名字

    # 获取城市对应的
    def get_area_code(self):
        if not os.path.exists("area_code.json"):
            url = "https://m.10010.com/king/kingNumCard/init?product=0&channel=611&WT.mc_id=jituan_wangka_1803_baidusem_401e66b6329c53dd&utm_source=baidusem&utm_medium=cpc&utm_content=textlink&utm_campaign=jituan_wangka_1803_baidusem_401e66b6329c53dd&bd_vid=11434467437403140638"
            response = requests.get(url)
            json_dict = json.loads(response.text)

            for province in json_dict["provinceData"]:
                provinceName = province["PROVINCE_NAME"]
                provinceCode = province["PROVINCE_CODE"]
                self.provinceCodeToName[provinceCode] = provinceName
                self.provinceNameToCode[provinceName] = provinceCode

            for provinceCode, cities in json_dict["cityData"].items():
                provinceName = self.provinceCodeToName[provinceCode]
                self.provinceNameToCityNameList[provinceName] = []
                for city in cities:
                    cityCode = city["CITY_CODE"]
                    cityName = city["CITY_NAME"]
                    self.cityCodeToName[cityCode] = cityName
                    self.cityNameToCode[cityName] = cityCode
                    self.provinceNameToCityNameList[provinceName].append(cityName)

            # 保存信息
            with open("area_code.json", 'w') as f:
                total_dict = {}
                total_dict['provinceCodeToName'] = self.provinceCodeToName
                total_dict['provinceNameToCode'] = self.provinceNameToCode
                total_dict['cityNameToCode'] = self.cityNameToCode
                total_dict['cityCodeToName'] = self.cityCodeToName
                total_dict['provinceNameToCityNameList'] = self.provinceNameToCityNameList
                json.dump(total_dict, f)

        else:
            # 保存信息
            with open("area_code.json", 'r') as f:
                total_dict = json.load(f)
                self.provinceCodeToName = total_dict['provinceCodeToName']
                self.provinceNameToCode = total_dict['provinceNameToCode']
                self.cityNameToCode = total_dict['cityNameToCode']
                self.cityCodeToName = total_dict['cityCodeToName']
                self.provinceNameToCityNameList = total_dict['provinceNameToCityNameList']

    def __init__(self):
        super().__init__()
        self.get_area_code()
        self.initUI()
        self.initListener()  # 初始化按钮的监听器

    def initUI(self):
        v_layout = QVBoxLayout()  # 总体布局是垂直布局
        self.province_list_combobox = QComboBox()
        self.city_list_combobox = QComboBox()
        self.add_task_button = QPushButton("添加任务")
        self.start_task_button = QPushButton("开始任务")
        self.delete_selected_button = QPushButton("删除选中任务")
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["省", "市"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)  # 多行选中

        h_layout = QHBoxLayout()
        h_widget = QWidget()
        h_widget.setLayout(h_layout)
        h_layout.addWidget(self.province_list_combobox)
        h_layout.addWidget(self.city_list_combobox)
        h_layout.addWidget(self.add_task_button)
        h_layout.addWidget(self.start_task_button)
        h_layout.addWidget(self.delete_selected_button)

        v_layout.addWidget(h_widget)
        v_layout.addWidget(self.tableWidget)
        self.setLayout(v_layout)

        self.province_list_combobox.addItem('全国')
        self.city_list_combobox.addItem('全部')
        self.province_list_combobox.addItems(self.provinceNameToCityNameList.keys())
        self.province_list_combobox.activated[str].connect(self.update_city_list_combobox)

    def update_city_list_combobox(self, province_name):
        self.city_list_combobox.clear()
        self.city_list_combobox.addItem('全部')
        self.city_list_combobox.addItems(self.provinceNameToCityNameList[province_name])

    def initListener(self):
        self.add_task_button.clicked.connect(self.onClickButtonAdd)
        self.start_task_button.clicked.connect(self.onClickButtonStart)
        self.delete_selected_button.clicked.connect(self.onClickButtonDelete)

    def onClickButtonDelete(self):
        # 删除tableWidget选中的行
        index_list = []
        for model_idx in self.tableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_idx)
            index_list.append(index)

        # 绝对不可以一边遍历一边删除，会删不完
        for index in index_list:
            self.logging_signal.emit(f"删除{self.tableWidget.item(index.row(), 0).text()}-"
                                     f"{self.tableWidget.item(index.row(), 1).text()}")
            self.tableWidget.removeRow(index.row())

    def onClickButtonStart(self):
        # 将任务发送给爬虫
        rowCount = self.tableWidget.rowCount()
        # 遍历每行
        if rowCount == 0:
            QMessageBox.information(self, "提示", f"请先添加任务")
            return

        for row_idx in range(rowCount):
            provinceName = self.tableWidget.item(row_idx, 0).text()
            cityName = self.tableWidget.item(row_idx, 1).text()
            print("添加任务:", provinceName, cityName)

            self.add_task_signal.emit({"provinceCode": self.provinceNameToCode[provinceName],
                                       "cityCode": self.cityNameToCode[cityName],
                                       "cityName": cityName,
                                       "provinceName": provinceName})

        self.logging_signal.emit(f"新添加{rowCount}条任务")
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

    # 添加任务按钮
    def onClickButtonAdd(self):
        thread = Thread(target=self.add_task_thread)
        thread.start()

    def add_task_thread(self):
        # 先禁用掉这个按钮避免没添加完
        self.add_task_button.setEnabled(False)
        self.start_task_button.setEnabled(False)
        self.start_task_button.setText("正在添加任务...")

        # # 先获取当前选中的省份名字
        provinceNameSelected = self.province_list_combobox.currentText()
        cityNameSelected = self.city_list_combobox.currentText()
        if provinceNameSelected == "全国":
            # 添加全国的任务
            for province in self.provinceNameToCityNameList.keys():
                for city in self.provinceNameToCityNameList[province]:
                    self.add_task_to_tableWidget(province, city)

        else:
            # 添加一个省的全部市
            if cityNameSelected == "全部":
                for city in self.provinceNameToCityNameList[provinceNameSelected]:
                    self.add_task_to_tableWidget(provinceNameSelected, city)
            else:
                self.add_task_to_tableWidget(provinceNameSelected, cityNameSelected)

        #
        self.add_task_button.setEnabled(True)
        self.start_task_button.setEnabled(True)
        self.start_task_button.setText("开始任务")
        self.logging_signal.emit("添加任务完成,请删除自己不需要的任务,然后点击[开始任务]按钮")


    # 将新添加的任务显示到tableWidget上面去
    def add_task_to_tableWidget(self, provinceName, cityName):
        rowCount = self.tableWidget.rowCount()
        # # 必须先插入一行
        self.tableWidget.insertRow(rowCount)
        # # # 准备数据
        self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(provinceName))
        self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(cityName))
        self.tableWidget.resizeColumnsToContents()  # 调整列适应内容


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = AddTaskWidget()
    main.show()

    sys.exit(app.exec_())
