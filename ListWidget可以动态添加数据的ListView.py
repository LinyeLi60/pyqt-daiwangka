from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel
import sys

class ListWidget(QWidget):

    def __init__(self):
        super(ListWidget, self).__init__()
        self.setWindowTitle("QTableView表格视图控件演示")
        self.resize(500, 300)

        self.listwidget = QListWidget()
        self.listwidget.resize(300, 120)
        self.listwidget.addItem("111")
        self.listwidget.addItem("222")
        self.listwidget.addItem("333")
        self.listwidget.itemClicked.connect(self.clicked)     # 不可以用

        layout = QVBoxLayout()
        layout.addWidget(self.listwidget)

        self.setLayout(layout)

    def clicked(self, data):
        QMessageBox.information(self, "QListView", "您选择了:" + self.listwidget.item(self.listwidget.row(data)).text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = ListWidget()
    main.show()

    sys.exit(app.exec_())