from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import requests
import json
import os
from PyQt5.QtCore import QThread, pyqtSignal


# 自定义规则
class CustomRuleWidget(QWidget):

    customRulesSender = pyqtSignal(list)     # 发送自定义规则的列表

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initListener()

    def initUI(self):
        v_layout = QVBoxLayout()
        label = QLabel("自定义规则设置")
        # label.setAlignment(QtCore.Qt.AlignHCenter)
        v_layout.addWidget(label)
        label_1 = QLabel("间隔符:@  11位号码不确定的用*表示, 如1234结尾的请填写1******1234")
        # label_1.setAlignment(QtCore.Qt.AlignHCenter)
        v_layout.addWidget(label_1)
        self.checkbox = QCheckBox("开启自定义规则")

        v_layout.addWidget(self.checkbox, QtCore.Qt.AlignHCenter)

        self.textEdit = QPlainTextEdit("1******7521@1******1314")
        v_layout.addWidget(self.textEdit)
        self.setLayout(v_layout)

    def initListener(self):
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)

    def checkbox_state_changed(self):
        if self.checkbox.isChecked():
            # 首先检查一下自定义规则是否正确
            ret_code, message = self.check_custom_rule()
            if not ret_code:
                QMessageBox.information(self, "错误", message)
                self.checkbox.setChecked(False)

            else:
                # 设置成功了
                # QMessageBox.information(self, "提示", message)
                self.textEdit.setReadOnly(True)
                self.customRulesSender.emit(self.textEdit.toPlainText().split("@"))
        else:
            self.textEdit.setReadOnly(False)
            self.customRulesSender.emit([])     # 把规则清空

    def check_custom_rule(self):
        try:
            for item in self.textEdit.toPlainText().split("@"):
                assert len(item) == 11, '自定义规则长度未满11位'
                assert item.replace('*', '').isdigit() is True, '出现非法字符'
        except Exception as e:
            return False, str(e)
        return True, "开启自定义规则成功"


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = CustomRuleWidget()
    main.show()

    sys.exit(app.exec_())


