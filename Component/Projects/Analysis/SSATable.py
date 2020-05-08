from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QLabel, QVBoxLayout, QAction, QMenuBar
from PyQt5.QtCore import Qt
from Component.Materials import Checkbox
from Component.Materials import CheckboxItem
from Connector.LogicSSA import ReturnSSA

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class SSATable(QWidget):
    def __init__(self, db_name, tab_project):
        QWidget.__init__(self)
        self.tab_project = tab_project
        self.__return_ssa__ = ReturnSSA(db_name)
        self.db_name = db_name
        self.__variables__()
        self.__component__()

    def __variables__(self):
        self.columns = ['선택']+self.__return_ssa__.Columns()
        self.dataframe = self.__return_ssa__.Dataframe()
        self.checked = []

    def __component__(self):
        self.__menubar__()
        self.__table__()
        self.__layout__()

    def __menubar__(self):
        self.action_all = QAction('전체 선택', self)
        self.action_all.triggered.connect(self.All)
        self.menubar = QMenuBar(self)
        self.menubar.addAction(self.action_all)

    def All(self):
        if self.action_all.text() == '전체 선택':
            self.__select_all__()
        elif self.action_all.text() == '선택 해제':
            self.__unselect_all__()

    def __select_all__(self):
        row_count = self.table.rowCount()
        self.checked.clear()
        for row in range(row_count):
            self.table.cellWidget(row, 0).setChecked(True)
            if row != -1:
                self.checked.append(row)
        self.action_all.setText('선택 해제')

    def __unselect_all__(self):
        row_count = self.table.rowCount()
        for row in range(row_count):
            self.table.cellWidget(row, 0).setChecked(False)
        self.checked.clear()
        self.action_all.setText('전체 선택')

    def __checkbox__(self, table, row, col):
        checkboxitem = CheckboxItem()
        checkbox = Checkbox(checkboxitem)
        checkbox.clicked.connect(self.Checked)
        table.setItem(row, col, checkboxitem)
        table.setCellWidget(row, col, checkbox)

    def Checked(self, check):
        row = self.table.currentRow()
        if check:
            self.checked.append(row)
            self.action_all.setText('선택 해제')
        elif not check:
            self.checked.remove(row)
        if not self.checked:
            self.action_all.setText('전체 선택')

    def __table__(self):
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setAlternatingRowColors(True)
        style = "QHeaderView::section {font-weight: bold; border: 2px black;}"
        self.table.setStyleSheet(style)
        for row, lst in enumerate(self.dataframe.values):
            self.table.insertRow(row)
            self.table.setRowHeight(row, 50)
            self.__checkbox__(self.table, row, 0)
            for col, data in enumerate(lst):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemIsEditable)
                self.table.setItem(row, col + 1, item)
        self.table.hideColumn(1)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

    def __layout__(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('※ SSA 논리 정보\n'))
        layout.addWidget(self.menubar)
        layout.addWidget(self.table)
        self.setLayout(layout)