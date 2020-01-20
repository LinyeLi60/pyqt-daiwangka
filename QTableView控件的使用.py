from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class TableView(QWidget):

    def __init__(self):
        super(TableView, self).__init__()
        self.setWindowTitle("QTableView表格视图控件演示")
        self.resize(500, 300)

        self.model = QStandardItemModel(4, 3)
        self.model.setHorizontalHeaderLabels(['省份', '城市', '号码'])

        self.tableView = QTableView()
        # 关联QTableView控件和Model
        self.tableView.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)
        # 添加数据
        self.add_item()

    def add_item(self):
        item11 = QStandardItem("北京")
        item12 = QStandardItem("北京")
        item13 = QStandardItem("13777893886")
        self.model.setItem(0, 0, item11)
        self.model.setItem(0, 1, item12)
        self.model.setItem(0, 2, item13)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = TableView()
    main.show()

    sys.exit(app.exec_())