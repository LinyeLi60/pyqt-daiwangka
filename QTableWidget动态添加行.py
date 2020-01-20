from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel
import sys

class TableWidgetDemo(QMainWindow):
    def __init__(self):
        super(TableWidgetDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableWidget演示教程")
        self.resize(430, 230)

        # 添加一个退出窗口的button
        self.buttonAdd = QPushButton("添加一行数据")
        self.buttonAdd.clicked.connect(self.onClickButtonAdd)

        # 添加一个清空数据的button
        self.buttonClear = QPushButton("清空数据")
        self.buttonClear.clicked.connect(self.onClickButtonClear)


        # 添加QTableWidget对象
        self.tablewidget = QTableWidget()
        self.tablewidget.setColumnCount(3)
        self.tablewidget.setHorizontalHeaderLabels(["省份", '市', "号码"])
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)    # 禁止编辑
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)    # 选中整行
        self.tablewidget.horizontalHeader().setVisible(False)              # 隐藏水平表头
        self.tablewidget.verticalHeader().setVisible(False)              # 隐藏竖直表头



        layout = QVBoxLayout()
        layout.addWidget(self.tablewidget)
        layout.addWidget(self.buttonAdd)
        layout.addWidget(self.buttonClear)


        # 用一个widget来套布局
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

    def onClickButtonClear(self):
        self.tablewidget.clear()
        self.tablewidget.setRowCount(0)     # 一定要归0


    # 添加点击事件
    def onClickButtonAdd(self):
        rowCount = self.tablewidget.rowCount()

        # 必须先插入一行
        self.tablewidget.insertRow(rowCount)
        # 准备数据
        provinceItem = QTableWidgetItem("北京")
        self.tablewidget.setItem(rowCount, 0, provinceItem)

        cityItem = QTableWidgetItem("北京")
        self.tablewidget.setItem(rowCount, 1, cityItem)

        numberItem = QTableWidgetItem("13777893886")
        self.tablewidget.setItem(rowCount, 2, numberItem)
        self.tablewidget.resizeColumnsToContents()     # 调整列适应内容



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    main = TableWidgetDemo()
    main.show()

    sys.exit(app.exec_())
