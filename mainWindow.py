import datetime
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from typeGrid import TypeGridWidget
from spider import Spider
from addTaskWidget import AddTaskWidget
from ipConfigurationWidget import IPConfigurationWidget
from customRuleWidget import CustomRuleWidget

from orderInfoWidget import OrderInfoWidget
from buy import sendBuyRequest
from candidateWidget import CandidateWidget
from directlyBuyWidget import DirectlyBuyWidget


class MainGUI(QMainWindow):

    def __init__(self):
        super(MainGUI, self).__init__()
        self.spider = Spider()  # 新建一个爬虫类
        self.phone_number_count = 0
        self.phone_numbers = set()
        self.start_time = None      # 脚本启动时间

        self.type_grid_dict = {}  # 从名字映射到对应的widget
        self.initUI()

        # 连接信号与槽并且启动爬虫
        self.spider.sender.connect(self.displayNum)  # 现实号码
        self.addTaskTab.add_task_signal.connect(self.spider.add_single_task)  # 将添加任务菜单栏的信号与爬虫中添加任务的槽函数连起来
        self.ipTab.ip_url_setter.connect(self.spider.proxy_cleaner.set_ip_url)  # 设置ip代理的链接
        self.spider.proxy_cleaner.cleaned_ip_sender.connect(self.ipTab.displayCleanedProxy)  # 发给ipTab进行展示
        self.customRuleTab.customRulesSender.connect(self.spider.set_custom_rules)  # 设置自定义规则
        self.ipTab.thread_num_sender.connect(self.set_thread_num)
        self.candidateTab.buyNumberSender.connect(self.buy)
        self.directlyBuyTab.buyNumberSender.connect(self.buy)

        self.set_all_logging_signal()     # 把所有日志信号和主界面打印日志的连接在一起
        # 多对一信号槽连接
        for grid in self.type_grid_dict.values():
            grid.buyNumberSender.connect(self.buy)
            grid.addToCandidateSender.connect(self.addToCandidate)      # 添加到候选列表

    def addToCandidate(self, num, province, city, type_of_card, manually=False):
        """

        :param num: 号码
        :param province: 省份
        :param city: 城市
        :param type_of_card: 靓号类型
        :return:
        """
        self.logging(" ".join(["添加到候选名单:", num, province, city, type_of_card]))
        self.candidateTab.addCandidate(province=province, city=city, num=num, type_of_meal="腾讯王卡",
                                       type_of_number=type_of_card,
                                       add_time=datetime.datetime.now().strftime('%m-%d %H:%M:%S'), manually=manually)

    def set_thread_num(self):
        # 设置线程数量
        try:
            if self.spider.has_been_started:
                QMessageBox.information(self, "提示", "脚本已经启动过,无法设置线程!")
            else:
                thread_num = int(self.ipTab.thread_num_edit.text())
                self.spider.thread_num = thread_num
                self.logging(f"设置线程数为:{self.spider.thread_num}")
        except Exception as e:
            self.logging(str(e))
            QMessageBox.information(self, "错误", "线程数量应该为整数!")

    def setExperience(self):
        self.spider.thread_num = 50
        self.ipTab.buttonSetThread.setDisabled(True)
        self.ipTab.thread_num_edit.setText(f"体验模式线程数:{self.spider.thread_num}")
        self.ipTab.thread_num_edit.setReadOnly(True)
        self.ipTab.ip_url_edit.setText("体验模式请自己添加ip代理链接")
        self.spider.proxy_cleaner.set_ip_url("")
        self.customRuleTab.checkbox.setDisabled(True)
        self.customRuleTab.checkbox.setText("体验模式无法使用自定义规则")
        self.orderInfoTab.ui.lineEditName.setText("体验模式不可以设置下单用户信息")
        self.orderInfoTab.ui.lineEditName.setReadOnly(True)

    def set_all_logging_signal(self):
        self.spider.logging_signal.connect(self.logging)
        self.spider.proxy_cleaner.logging_signal.connect(self.logging)
        self.addTaskTab.logging_signal.connect(self.logging)
        self.candidateTab.logging_signal.connect(self.logging)

    def logging(self, text):
        self.log_edit_text.append(text+'\n')
        self.log_edit_text.moveCursor(QTextCursor.End)

    def displayNum(self, num, province, city, type_of_card_list, match_index_dict):
        self.phone_number_count += 1
        self.phone_numbers.add(num)
        # 计算出号频率
        duration = int(time.time()-self.start_time)
        count_per_second = int(self.phone_number_count / (duration+1))
        self.statusBar().showMessage(f'一共扫号靓号数量:{self.phone_number_count}, 经过去重后剩下:{len(self.phone_numbers)},'
                                     f'当前代理池代理数量:{self.spider.proxy_cleaner.proxy_num}, 出号频率:{count_per_second}个/秒')
        for type_of_card in type_of_card_list:
            if type_of_card in self.type_grid_dict:
                self.type_grid_dict[type_of_card].add_record(num, province, city, match_index_dict)  # 添加一行记录

    def initUI(self):
        self.statusBar().showMessage('扫号靓号数量:0')
        self.setWindowTitle("联通大王卡选号助手")
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

        self.checkbox_block_all = QCheckBox()      # 屏蔽所有
        self.checkbox_block_all.setChecked(False)    #
        self.checkbox_block_all.setText("全速冲")
        self.checkbox_block_all.stateChanged.connect(self.block_all_display)     #
        self.checkbox_multi_stage_schedule = QCheckBox()
        self.checkbox_multi_stage_schedule.setChecked(False)
        self.checkbox_multi_stage_schedule.setText("多级调度")
        self.checkbox_multi_stage_schedule.stateChanged.connect(self.multi_stage_schedule)  #

        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(self.checkbox_block_all)
        h_layout_1.addWidget(self.checkbox_multi_stage_schedule)
        h_widget_1 = QWidget()
        h_widget_1.setLayout(h_layout_1)
        h_widget_1.setFixedWidth(250)
        h_layout.addWidget(h_widget_1)

        h_layout.addWidget(self.buttonStart)
        h_layout.addWidget(self.buttonClearTask)
        h_layout.addWidget(self.buttonClearOutput)
        h_widget.setLayout(h_layout)

        for idx, name in enumerate(["所有号码", "自定义规则", "全段3A(AAA)", "尾号3拖1",
                                    "尾abababab", '*a*a*a*a',
                                    "真山", "顺子", "豹子", "尾号AAAAB", "倒顺",
                                    "5A", "中间4A", "尾号ABC", '尾号CBA', "ababab", "aaabbb",
                                    "中间ABCDE", "3数字组合", '1349风水号', 'AAABCD']):
            # 一行放5个
            if idx % 11 == 0:
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
        self.candidateTab = CandidateWidget()
        self.tabWidget.addTab(self.addTaskTab, "扫号设置")
        self.tabWidget.addTab(self.ipTab, "代理设置")
        self.tabWidget.addTab(self.customRuleTab, "自定义规则")
        self.orderInfoTab = OrderInfoWidget()
        self.tabWidget.addTab(self.orderInfoTab, "下单信息填写")
        self.tabWidget.addTab(self.candidateTab, "候选号码列表")
        self.directlyBuyTab = DirectlyBuyWidget()
        self.tabWidget.addTab(self.directlyBuyTab, "已知号码下单")

        h_layout.addWidget(self.tabWidget)
        self.log_edit_text = QTextEdit("日志信息")
        self.log_edit_text.setReadOnly(True)
        h_layout.addWidget(self.log_edit_text)

        layout.addWidget(h_widget)

        # 用一个widget来套布局
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

    def multi_stage_schedule(self):
        if self.checkbox_multi_stage_schedule.isChecked():
            self.logging("开启[多级调度],请在扫全国号码的时候打开多级调度,多级调度可智能屏蔽没有号码的地区")
            self.spider.open_multistage_scheduling = True
        else:
            self.logging("关闭[多级调度]")
            self.spider.open_multistage_scheduling = False

    def block_all_display(self):
        if self.checkbox_block_all.isChecked():
            self.logging("[全速冲]屏蔽所有号码显示,请手动取消单个类型的屏蔽")
            for grid in self.type_grid_dict.values():
                grid.checkBox.setChecked(True)
        else:
            self.logging("[全速冲]解除屏蔽所有号码显示,请手动添加单个类型的屏蔽")
            for grid in self.type_grid_dict.values():
                if grid.name != "所有号码":
                    grid.checkBox.setChecked(False)

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
            # 开始扫号之后线程数量就不可以更改了
            # 先检查一下任务是否都添加了
            if self.spider.is_task_empty():  # 如果任务是空的话
                QMessageBox.information(self, "任务为空", "①在扫号设置中添加任务\n②点击开始任务\n③点击开始扫号")
            else:
                self.start_time = time.time()  # 设置开始时间
                self.ipTab.thread_num_edit.setReadOnly(True)
                self.ipTab.buttonSetThread.setText("开始扫号后无法更改线程数量")
                self.ipTab.buttonSetThread.setEnabled(False)
                self.spider.carry_on()
                self.buttonStart.setText("停止")
        else:
            self.buttonStart.setText("开始扫号")
            self.spider.suspend()

    def onClickButtonClearAllOutput(self):
        for grid in self.type_grid_dict.values():
            grid.onClickButtonClear()

    def buy(self, number, province_name, city_name):
        self.logging(f"准备下单号码:{number}, {province_name},{city_name}")

        essProvince = self.addTaskTab.provinceNameToCode[province_name]
        essCity = self.addTaskTab.cityNameToCode[city_name]
        goodsId = "981702278573"
        webProvince = self.orderInfoTab.province_code
        webCity = self.orderInfoTab.city_code
        webCounty = self.orderInfoTab.county_code
        address = self.orderInfoTab.ui.lineEditLocation.text()
        certName = self.orderInfoTab.ui.lineEditName.text()
        certId = self.orderInfoTab.ui.lineEditIdCard.text()
        contractPhone = self.orderInfoTab.ui.lineEditContactPhone.text()
        # 直接写下单函数
        res_text = sendBuyRequest(essProvince, essCity, number, goodsId, webProvince, webCity, webCounty, address,
                                  certName,
                                  certId, contractPhone)
        self.log_edit_text.append('----------下单结果----------\n')
        self.log_edit_text.append(f'所选号码:{number}, 省:{province_name}, 市:{city_name}\n')
        self.log_edit_text.append(res_text)
        self.log_edit_text.append('-' * 50 + '\n')
        QMessageBox.information(self, "下单结果", res_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    main = MainGUI()
    main.showMaximized()

    sys.exit(app.exec_())
