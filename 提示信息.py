import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QPushButton, QHBoxLayout, QToolTip
from PyQt5.QtGui import QFont

class TooltipForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 12))
        self.setToolTip('今天是<b>星期六</b>')
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle("设置控件提示信息")

        # 添加一个退出窗口的button
        self.button = QPushButton("退出应用程序")
        self.button.setToolTip('这是一个按钮')    # 鼠标移到上面时会提示

        layout = QHBoxLayout()
        layout.addWidget(self.button)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = TooltipForm()
    main.show()

    sys.exit(app.exec_())