import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
import sys


class FirstMainWin(QMainWindow):
    def __init__(self, parent=None):
        super(FirstMainWin, self).__init__(parent)

        self.setWindowTitle("第一个主窗口应用")
        self.resize(400, 300)

        self.status = self.statusBar()
        self.status.showMessage("5秒消息", 5000)     #

        self.toCenter()

        # 添加一个退出窗口的button
        self.button = QPushButton("退出应用程序")
        self.button.clicked.connect(self.onClickButton)

        layout = QHBoxLayout()
        layout.addWidget(self.button)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)


    # 添加点击事件
    def onClickButton(self):
        sender = self.sender()
        print("按钮被按下")
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    # 窗口居中
    def toCenter(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft, newTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("snoopy.png"))

    main = FirstMainWin()
    main.show()

    sys.exit(app.exec_())