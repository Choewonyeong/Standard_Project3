from PyQt5.QtWidgets import QCheckBox, QTableWidgetItem
from PyQt5.QtCore import Qt

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Checkbox(QCheckBox):
    def __init__(self, item):
        super().__init__()
        self.setStyleSheet("QCheckBox {margin-left: 10px;}")
        self.item = item
        self.checkvalue = 0
        self.stateChanged.connect(self.checkbox_Changed)
        self.stateChanged.connect(self.item.setdata)

    def checkbox_Changed(self, checkvalue):
        self.checkvalue = checkvalue

    def getRow(self):
        return self.item.row()


class CheckboxItem(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setData(Qt.UserRole, 0)

    def setdata(self, value):
        self.setData(Qt.UserRole, value)