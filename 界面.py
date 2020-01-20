from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel
import sys
from typeGrid import TypeGridWidget
from spider import Spider
import random
from addTaskWidget import AddTaskWidget
from ipConfigurationWidget import IPConfigurationWidget
from customRuleWidget import CustomRuleWidget

from orderInfoWidget import OrderInfoWidget


class TableWidgetDemo(QMainWindow):

    def __init__(self):
        super(TableWidgetDemo, self).__init__()
        self.spider = Spider()  # 新建一个爬虫类
        self.phone_number_count = 0
        self.phone_numbers = set()

        self.type_grid_dict = {}  # 从名字映射到对应的widget
        self.initUI()

        # 连接信号与槽并且启动爬虫
        self.spider.sender.connect(self.displayNum)  # 现实号码
        self.addTaskTab.add_task_signal.connect(self.spider.add_single_task)     # 将添加任务菜单栏的信号与爬虫中添加任务的槽函数连起来
        self.ipTab.ip_url_setter.connect(self.spider.proxy_cleaner.set_ip_url)     # 设置ip代理的链接
        self.spider.proxy_cleaner.cleaned_ip_sender.connect(self.ipTab.displayCleanedProxy)                     # 发给ipTab进行展示
        self.customRuleTab.customRulesSender.connect(self.spider.set_custom_rules)                          # 设置自定义规则
        # 设置线程数量
        try:
            thread_num = int(self.ipTab.thread_num_edit.text())
            self.spider.thread_num = thread_num
        except Exception as e:
            QMessageBox.information(self, "错误", "线程数量应该为整数!")

    def displayNum(self, num, province, city, type_of_card_list, match_index_dict):
        self.phone_number_count += 1
        self.phone_numbers.add(num)
        self.statusBar().showMessage(f'一共扫号靓号数量:{self.phone_number_count}, 经过去重后剩下:{len(self.phone_numbers)}')
        for type_of_card in type_of_card_list:
            if type_of_card in self.type_grid_dict:
                self.type_grid_dict[type_of_card].add_record(num, province, city, match_index_dict)  # 添加一行记录

    def initUI(self):
        self.statusBar().showMessage('扫号靓号数量:0')
        self.setWindowTitle("联通大王卡选号助手, 微信:lly19980726")
        self.resize(800, 800)

        layout = QVBoxLayout()
        # 添加一个退出窗口的button
        h_layout = QHBoxLayout()
        h_widget = QWidget()
        self.buttonStart = QPushButton("开始扫号")
        self.buttonStart.clicked.connect(self.onClickButtonStart)
        self.buttonClearTask = QPushButton("清除当前所有任务, 请先点击停止按钮")
        self.buttonClearTask.clicked.connect(self.onClickButtonClearAllTask)
        self.buttonClearOutput = QPushButton("清除所有框框中的号码")
        self.buttonClearOutput.clicked.connect(self.onClickButtonClearAllOutput)
        h_layout.addWidget(self.buttonStart)
        h_layout.addWidget(self.buttonClearTask)
        h_layout.addWidget(self.buttonClearOutput)
        h_widget.setLayout(h_layout)

        for idx, name in enumerate(["所有号码", "自定义规则", "真山", "顺子", "豹子", "尾号AAAAB", "倒顺",
                                    "5A", "中间4A", "0001或0008", "XXX8", "ababab", "aaabbb",
                                    "中间ABCDE", "AA88", "3数字组合"]):
            # 一行放5个
            if idx % 8 == 0:
                bottom_widget = QWidget()
                bottom_layout = QHBoxLayout()
                bottom_widget.setLayout(bottom_layout)
                layout.addWidget(bottom_widget)


            type_grid_widget = TypeGridWidget(name)
            if name == "所有号码":
                type_grid_widget.checkBox.setChecked(True)

            self.type_grid_dict[name] = type_grid_widget
            bottom_layout.addWidget(type_grid_widget)

        layout.addWidget(h_widget)
        # 最下面的tab列表, 用于切换不同的功能

        h_layout = QHBoxLayout()
        h_widget = QWidget()
        h_widget.setLayout(h_layout)
        self.tabWidget = QTabWidget()
        self.addTaskTab = AddTaskWidget()
        self.ipTab = IPConfigurationWidget()
        self.customRuleTab = CustomRuleWidget()
        self.tabWidget.addTab(self.addTaskTab, "扫号设置")
        self.tabWidget.addTab(self.ipTab, "ip代理设置/线程数量设置")
        self.tabWidget.addTab(self.customRuleTab, "自定义规则")
        self.tabWidget.addTab(OrderInfoWidget(), "下单信息填写")
        h_layout.addWidget(self.tabWidget)
        self.log_edit_text = QTextEdit("日志信息")
        h_layout.addWidget(self.log_edit_text)


        layout.addWidget(h_widget)


        # 用一个widget来套布局
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

    def onClickButtonClearAllTask(self):
        # 如果当前还没暂停
        if self.buttonStart.text() == "停止":
            QMessageBox.information(self, "提示", "请先停止任务")

        else:
            if self.spider.is_task_empty():
                QMessageBox.information(self, "任务为空", "当前任务为空")
            else:
                #
                self.spider.remove_all_task()
                QMessageBox.information(self, "清空任务", "清空所有任务完成, 你自己添加新任务")

    # 添加点击事件
    def onClickButtonStart(self):
        if self.buttonStart.text() == "开始扫号":
            # 先检查一下任务是否都添加了
            if self.spider.is_task_empty():     # 如果任务是空的话
                QMessageBox.information(self, "任务为空", "①在扫号设置中添加任务\n②点击开始任务\n③点击开始扫号")
            else:
                self.spider.carry_on()
                self.buttonStart.setText("停止")
        else:
            self.buttonStart.setText("开始扫号")
            self.spider.suspend()

    def onClickButtonClearAllOutput(self):
        for grid in self.type_grid_dict.values():
            grid.onClickButtonClear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    main = TableWidgetDemo()
    main.showMaximized()

    sys.exit(app.exec_())
