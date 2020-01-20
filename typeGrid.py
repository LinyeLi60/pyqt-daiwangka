from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
try:
    from html import escape
except ImportError:
    from cgi import escape
    
import sys

class HTMLDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HTMLDelegate, self).__init__(parent)
        self.doc = QTextDocument(self)

    def paint(self, painter, option, index):
        substring = index.data(Qt.UserRole)
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        res = ""
        color = QColor("red")
        if substring:
            substrings = options.text.split(substring)
            res = """<font color="{}">{}</font>""".format(
                color.name(QColor.HexRgb), substring
            ).join(list(map(escape, substrings)))
        else:
            res = escape(options.text)
        self.doc.setHtml(res)

        options.text = ""
        style = (
            QApplication.style()
            if options.widget is None
            else options.widget.style()
        )
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.State_Selected:
            ctx.palette.setColor(
                QPalette.Text,
                option.palette.color(
                    QPalette.Active, QPalette.HighlightedText
                ),
            )
        else:
            ctx.palette.setColor(
                QPalette.Text,
                option.palette.color(QPalette.Active, QPalette.Text),
            )

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)

        thefuckyourshitup_constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - thefuckyourshitup_constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)

        painter.restore()


class TypeGridWidget(QWidget):

    def __init__(self, name, width=300, height=300):
        super().__init__()
        self.resize(width, height)
        self.name = name     # 靓号类型
        self.initUI()
        self.initListener()     # 一些点击事件

    def initUI(self):
        layout = QVBoxLayout()
        label = QLabel(self.name)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["号码", "市", "省份"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏竖直表头
        self.tableWidget.setItemDelegate(HTMLDelegate(self.tableWidget))

        # 底部按钮
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        self.checkBox = QCheckBox()
        labelHint = QLabel("勾选则不显示")
        self.buttonClear = QPushButton("清空")
        bottom_layout.addWidget(self.checkBox)
        bottom_layout.addWidget(labelHint)
        bottom_layout.addWidget(self.buttonClear)
        bottom_widget.setLayout(bottom_layout)

        # 添加所有控件
        layout.addWidget(label)
        layout.addWidget(self.tableWidget)
        layout.addWidget(bottom_widget)
        self.setLayout(layout)

    def initListener(self):
        self.buttonClear.clicked.connect(self.onClickButtonClear)

    def onClickButtonClear(self):
        print(f"清空所有{self.name}")
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)     # 一定要归0

    def add_record(self, num, province, city, match_index_dict):
        # 如果不展示号码
        if self.checkBox.isChecked():
            return

        item_num = QTableWidgetItem(num)
        if self.name in match_index_dict:
            s, e = match_index_dict[self.name]     # 下标索引
            text = num[s: e]
            print(self.name, text)
            item_num.setData(Qt.UserRole, text)

        rowCount = self.tableWidget.rowCount()
        # # 必须先插入一行
        self.tableWidget.insertRow(rowCount)
        # # # 准备数据
        self.tableWidget.setItem(rowCount, 0, item_num)
        self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(city))
        self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(province))
        self.tableWidget.resizeColumnsToContents()  # 调整列适应内容
        self.tableWidget.scrollToBottom()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = TypeGridWidget("真山")
    main.show()

    sys.exit(app.exec_())
