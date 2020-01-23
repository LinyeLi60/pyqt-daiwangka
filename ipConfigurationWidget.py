from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import requests
import json
import os
from PyQt5.QtCore import QThread, pyqtSignal


# 添加任务的widget
from proxy_utils import validate_url


class IPConfigurationWidget(QWidget):
    ip_url_setter = pyqtSignal(str)  # 把ip代理的链接发出去
    thread_num_sender = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initListener()

    def displayCleanedProxy(self, proxy):
        if self.ip_list.count() > 100:
            self.ip_list.clear()
        self.ip_list.addItem(proxy)
        self.ip_list.setCurrentRow(self.ip_list.count()-1)    # 自动往下滚动


    def initUI(self):
        h_layout = QHBoxLayout()  # 总体布局是垂直布局

        v_layout = QVBoxLayout()
        v_widget = QWidget()
        self.ip_url_edit = QLineEdit("http://www.15daili.com/apiProxy.ashx?un=13777893886&pw=5201314.&count=500")
        self.buttonSetThread = QPushButton("设置线程数/请在开启脚本之前设置")
        self.buttonValidate = QPushButton("测试IP")
        self.buttonSet = QPushButton("设置当前IP代理进行扫号")
        self.thread_num_edit = QLineEdit("100")      # 线程数量设置
        thread_num_label = QLabel("线程数量:  ")

        h_layout_1 = QHBoxLayout()
        h_widget_1 = QWidget()
        h_widget_1.setLayout(h_layout_1)
        h_layout_1.addWidget(thread_num_label)
        h_layout_1.addWidget(self.thread_num_edit)

        h_layout_2 = QHBoxLayout()
        h_widget_2 = QWidget()
        h_widget_2.setLayout(h_layout_2)
        ip_label = QLabel("ip代理链接:")
        h_layout_2.addWidget(ip_label)
        h_layout_2.addWidget(self.ip_url_edit)

        v_layout.addWidget(h_widget_1)
        v_layout.addWidget(h_widget_2)
        v_layout.addWidget(self.buttonSetThread)
        v_layout.addWidget(self.buttonValidate)
        v_layout.addWidget(self.buttonSet)
        v_widget.setLayout(v_layout)
        self.ip_list = QListWidget()
        h_layout.addWidget(v_widget)
        h_layout.addWidget(self.ip_list)
        self.setLayout(h_layout)

    def initListener(self):
        self.buttonValidate.clicked.connect(self.validate_url_listener)      # 验证并启动ip清洗
        self.buttonSet.clicked.connect(self.set_url)  # 验证并启动ip清洗
        self.buttonSetThread.clicked.connect(self.set_thread_num)       # 设置线程数量

    def set_thread_num(self):
        self.thread_num_sender.emit(self.thread_num_edit.text())

    def set_url(self):
        # 先验证一下连接是否有效
        self.validate_url_listener()
        # 然后把链接发出去
        self.ip_url_setter.emit(self.ip_url_edit.text())

    def validate_url_listener(self):

        # "http://www.15daili.com/apiProxy.ashx?un=13777893886&pw=5201314.&count=500"
        url = self.ip_url_edit.text()
        if url[:4] != "http":
            QMessageBox.information(self, "错误", "ip代理连接格式不正确!!!")
        else:
            # 创建一个线程去校验ip能否返回东西
            QMessageBox.information(self, "提示", validate_url(url))




if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = IPConfigurationWidget()
    main.show()

    sys.exit(app.exec_())
