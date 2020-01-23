
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from typeGrid import TypeGridWidget


# 多方格
class MultiGridWidget(QWidget):

    sub_window_count = 0

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.mdi_area = QMdiArea()
        layout = QVBoxLayout()
        layout.addWidget(self.mdi_area)
        self.setLayout(layout)

        for idx, name in enumerate(["所有号码", "自定义规则", "全段3A(AAA)", "尾号3拖1",
                                    "尾abababab", '*a*a*a*a',
                                    "真山", "顺子", "豹子", "尾号AAAAB", "倒顺",
                                    "5A", "中间4A", "尾号ABC", '尾号CBA', "ababab", "aaabbb",
                                    "中间ABCDE", "3数字组合", '1349风水号', 'AAABCD']):

            type_grid_widget = TypeGridWidget(name)
            self.sub_window_count += 1     # 子窗口数量+1
            sub_window = QMdiSubWindow()
            sub_window.setWidget(type_grid_widget)
            self.mdi_area.addSubWindow(sub_window)
            sub_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MultiGridWidget()
    main.show()

    sys.exit(app.exec_())