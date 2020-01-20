from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class TabWidgetDemo(QTabWidget):

    def __init__(self):
        super(QTabWidget, self).__init__()
        self.setWindowTitle("选项卡控件：QTabWidget")

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, '选项卡1')
        self.addTab(self.tab2, '选项卡2')
        self.addTab(self.tab3, '选项卡3')

        self.tab1UI()     # 设置选项卡的UI

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow('姓名', QLineEdit())
        layout.addRow('地址', QLineEdit())
        self.tab1.setLayout(layout)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    main = TabWidgetDemo()
    main.show()

    sys.exit(app.exec_())