from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QStringListModel
import sys

class ListView(QWidget):

    def __init__(self):
        super(ListView, self).__init__()
        self.setWindowTitle("QTableView表格视图控件演示")
        self.resize(500, 300)

        layout = QVBoxLayout()
        listView = QListView()
        listModel = QStringListModel()
        self.list = ['省份', '城市', '号码']

        listModel.setStringList(self.list)
        listView.setModel(listModel)              # 设置模型
        listView.clicked.connect(self.clicked)    # 添加槽函数

        layout.addWidget(listView)
        self.setLayout(layout)


    def clicked(self, item):
        QMessageBox.information(self, "QListView", "您选择了:" + self.list[item.row()])


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = ListView()
    main.show()

    sys.exit(app.exec_())