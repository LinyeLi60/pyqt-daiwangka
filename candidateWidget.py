from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class CandidateWidget(QMainWindow):

    buyNumberSender = pyqtSignal(str, str, str)
    logging_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.phone_numbers = set()
        self.initUI()

    def initUI(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["勾选", "省", "市", "号码", "套餐", "靓号类型", "添加时间"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        # 设置右键出现菜单
        self.items = QDockWidget('双击变成浮动窗口|双击恢复到原来位置', self)
        self.items.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)
        self.items.setWidget(self.tableWidget)
        self.setCentralWidget(self.items)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.items)

        # 设置右键出现菜单
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showContextMenu)

        # 新建一个菜单栏
        self.contextMenu = QMenu()
        self.actionBuy = self.contextMenu.addAction("一键下单")
        self.actionBuy.triggered.connect(self.actionBuyHandler)
        self.actionCopy = self.contextMenu.addAction("复制(shift键进行多选后复制)")
        self.actionCopy.triggered.connect(self.actionCopyHandler)
        self.actionDelete = self.contextMenu.addAction("删除")
        self.actionDelete.triggered.connect(self.actionDeleteHandler)
        self.actionSelectAll = self.contextMenu.addAction("预选列表[选中全部]")
        self.actionSelectAll.triggered.connect(self.actionSelectAllHandler)
        self.actionCancelAll = self.contextMenu.addAction("预选列表[取消全部]")
        self.actionCancelAll.triggered.connect(self.actionCancelAllHandler)
        # 复制所有选中的
        self.actionCopySelected = self.contextMenu.addAction("复制所有勾选号码")
        self.actionCopySelected.triggered.connect(self.actionCopySelectedHandler)

        self.actionDeleteSelected = self.contextMenu.addAction("预选列表[删除选中]")
        self.actionDeleteSelected.triggered.connect(self.actionDeleteSelectedHandler)


    def addCandidate(self, province, city, type_of_meal, type_of_number, num, add_time, manually=False):
        """

        :param province:
        :param city:
        :param type_of_meal: 套餐类型
        :param type_of_number: 靓号类型
        :param num:
        :param add_time:
        :return:
        """
        # 如果号码已经出现过了并且不是手动添加
        if num in self.phone_numbers and not manually:
            return
        self.phone_numbers.add(num)

        # 添加候选名单
        rowCount = self.tableWidget.rowCount()
        # # 必须先插入一行
        self.tableWidget.insertRow(rowCount)
        # # # 准备数据
        index_check_box = QCheckBox()

        self.tableWidget.setCellWidget(rowCount, 0, index_check_box)
        self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(province))
        self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(city))
        self.tableWidget.setItem(rowCount, 3, QTableWidgetItem(num))
        self.tableWidget.setItem(rowCount, 4, QTableWidgetItem(type_of_meal))
        self.tableWidget.setItem(rowCount, 5, QTableWidgetItem(type_of_number))
        self.tableWidget.setItem(rowCount, 6, QTableWidgetItem(add_time))
        self.setUpdatesEnabled(True)
        self.tableWidget.resizeColumnsToContents()  # 调整列适应内容
        if self.contextMenu.isHidden():
            self.tableWidget.scrollToBottom()     # 不要滚动

    def actionCopySelectedHandler(self):
        index_list = []
        for row_idx in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(row_idx, 0).isChecked():
                index_list.append(row_idx)

        copy_text = ""
        for row_idx in index_list:
            provinceName = self.tableWidget.item(row_idx, 1).text()
            cityName = self.tableWidget.item(row_idx, 2).text()
            number = self.tableWidget.item(row_idx, 3).text()
            type_of_number = self.tableWidget.item(row_idx, 5).text()
            line = f"{provinceName} {cityName} {number} {type_of_number}\n"
            copy_text += line

        clipboard = QApplication.clipboard()
        clipboard.setText(copy_text)

    def actionDeleteHandler(self):
        index_list = []
        for model_idx in self.tableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_idx)
            index_list.append(index)

        # 绝对不可以一边遍历一边删除，会删不完
        for index in index_list:
            self.logging_signal.emit(f"从候选区删除{self.tableWidget.item(index.row(), 3).text()}")
            self.tableWidget.removeRow(index.row())

    def actionDeleteSelectedHandler(self):
        index_list = []
        for row_idx in range(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(row_idx, 0).isChecked():
                index_list.append(row_idx)

        # print(index_list)
        # 绝对不可以一边遍历一边删除，会删不完
        for row_idx in index_list[::-1]:
            self.tableWidget.removeRow(row_idx)

    def actionSelectAllHandler(self):
        rowCount = self.tableWidget.rowCount()
        for row_idx in range(rowCount):
            self.tableWidget.cellWidget(row_idx, 0).setChecked(True)

    def actionCancelAllHandler(self):
        rowCount = self.tableWidget.rowCount()
        for row_idx in range(rowCount):
            self.tableWidget.cellWidget(row_idx, 0).setChecked(False)

    def showContextMenu(self, position):
        """

        :param position: 右键点击的位置
        :return:
        """
        # 行数大于0才可以

        if self.tableWidget.rowCount() > 0:
            self.contextMenu.move(QCursor().pos())
            self.contextMenu.show()


    def actionBuyHandler(self):
        for i in self.tableWidget.selectionModel().selection().indexes():
            rowNum = i.row()

        provinceName = self.tableWidget.item(rowNum, 1).text()
        cityName = self.tableWidget.item(rowNum, 2).text()
        waitToBuyNumber = self.tableWidget.item(rowNum, 3).text()
        print("待下单:", waitToBuyNumber, provinceName, cityName)
        self.buyNumberSender.emit(waitToBuyNumber, provinceName, cityName)

    def actionCopyHandler(self):

        index_list = []
        for model_idx in self.tableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_idx)
            index_list.append(index.row())

        copy_text = ""
        for row_idx in index_list:
            provinceName = self.tableWidget.item(row_idx, 1).text()
            cityName = self.tableWidget.item(row_idx, 2).text()
            number = self.tableWidget.item(row_idx, 3).text()
            type_of_number = self.tableWidget.item(row_idx, 5).text()
            line = f"{provinceName} {cityName} {number} {type_of_number}\n"
            copy_text += line

        clipboard = QApplication.clipboard()
        clipboard.setText(copy_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = CandidateWidget()
    main.show()

    main.addCandidate("1", "2", "3", "4", "5", "6")
    main.addCandidate("1", "2", "3", "4", "5", "6")
    main.addCandidate("1", "2", "3", "4", "5", "6")

    sys.exit(app.exec_())