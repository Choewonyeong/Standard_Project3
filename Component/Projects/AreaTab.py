from PyQt5.QtWidgets import QWidget, QAction, QMenuBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Component.Materials import Checkbox
from Component.Materials import CheckboxItem
from Connector.FireArea import ConnectorArea
from Connector.FireArea import ReturnArea

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class AreaTab(QWidget):
    def __init__(self, db_name, tab_project, method):
        QWidget.__init__(self)
        self.tab_project = tab_project
        self.method = method
        self.__connector_area__ = ConnectorArea(db_name)
        self.__return_area__ = ReturnArea(db_name)
        self.db_name = db_name
        self.__variables__()
        self.__component__()

    def __variables__(self):
        self.columns = ['선택']+self.__return_area__.Columns()
        self.dataframe = self.__return_area__.Dataframe()
        self.checked = []
        self.edited = []

    def __component__(self):
        self.__menubar__()
        self.__table__()
        self.__layout__()

    def __menubar__(self):
        action_insert = QAction('추가', self)
        action_insert.setShortcut('Alt+1')
        action_delete = QAction('삭제', self)
        action_delete.setShortcut('Alt+2')
        action_save = QAction('저장', self)
        action_save.setShortcut('Ctrl+S')
        action_insert.triggered.connect(self.Insert)
        action_delete.triggered.connect(self.Delete)
        action_save.triggered.connect(self.Save)
        self.menubar = QMenuBar(self)
        self.menubar.addAction(action_insert)
        self.menubar.addAction(action_delete)
        self.menubar.addAction(action_save)

    def Insert(self):
        row = self.table.rowCount()
        if row == 0:
            number = 1
        elif row != 0:
            number = int(self.table.item(row-1, 1).text())+1
        item = QTableWidgetItem(str(number))
        item.setFlags(Qt.ItemIsEditable)
        item.setTextAlignment(Qt.AlignCenter)
        self.table.insertRow(row)
        self.table.setRowHeight(row, 50)
        self.__checkbox__(self.table, row, 0)
        self.table.setItem(row, 1, item)
        item = QTableWidgetItem('')
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item)
        for col in range(3, 5):
            item = QTableWidgetItem('')
            self.table.setItem(row, col, item)
        self.__connector_area__.Insert(number)

    def __except__(self, row):
        for edited in self.edited:
            if row == edited[0]:
                self.edited.remove(edited)

    def Delete(self):
        self.checked.sort(reverse=True)
        for row in self.checked:
            self.__except__(row)
            number = int(self.table.item(row, 1).text())
            self.__connector_area__.Delete(number)
            self.table.removeRow(row)
        self.checked.clear()

    def Save(self):
        edited = list(set(map(tuple, self.edited)))
        for row, col in edited:
            number = int(self.table.item(row, 1).text())
            if col == 2:
                value = self.table.item(row, col).text()
                self.__connector_area__.Update(number, '방화지역번호', value)
            elif col == 3:
                value = self.table.item(row, col).text()
                self.__connector_area__.Update(number, '방화지역명', value)
            elif col == 4:
                value = self.table.item(row, col).text()
                self.__connector_area__.Update(number, '격실정보', value)
            elif col == 5:
                value = self.table.item(row, col).text()
                self.__connector_area__.Update(number, '비고', value)
        self.edited.clear()
        self.method()

    def __checkbox__(self, table, row, col):
        checkboxitem = CheckboxItem()
        checkbox = Checkbox(checkboxitem)
        checkbox.stateChanged.connect(self.Checked)
        table.setItem(row, col, checkboxitem)
        table.setCellWidget(row, col, checkbox)

    def Checked(self, check):
        row = self.table.currentRow()
        if check == 2:
            self.checked.append(row)
        elif check == 0:
            self.checked.remove(row)

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
                if col == 0:
                    item = QTableWidgetItem(str(data))
                    item.setFlags(Qt.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignCenter)
                elif col == 1:
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem(str(data))
                self.table.setItem(row, col+1, item)
        self.table.hideColumn(1)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellChanged.connect(self.Edited)

    def Edited(self, row, col):
        if col != 0:
            self.edited.append([row, col])

    def __layout__(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('※ 방화지역 정보\n'))
        layout.addWidget(self.menubar)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Delete:
            row = self.table.currentRow()
            col = self.table.currentColumn()
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, col, item)