from PyQt5.QtWidgets import QWidget, QAction, QMenuBar, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget
from PyQt5.QtWidgets import QFileDialog, QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from Component.Projects.Analysis.AreaTable import AreaTable
from Component.Projects.Analysis.MSOTable import MSOTable
from Component.Projects.Analysis.SSATable import SSATable
from Component.Projects.Analysis.MSOSetup import MSOSetup
from Component.Projects.Analysis.SSASetup import SSASetup
from Component.Projects.Analysis.SaveResult import SaveResult
from Connector.TabSetting import TabSetting

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class AnalysTab(QWidget):
    def __init__(self, db_name, tab_project, method):
        QWidget.__init__(self)
        self.tab_project = tab_project
        self.method = method
        self.db_name = db_name
        self.__connect_tabidx__ = TabSetting()
        self.__component__()

    def __component__(self):
        self.__menubar_mso__()
        self.__menubar_ssa__()
        self.__tables__()
        self.__table_result_mso__()
        self.__table_result_ssa__()
        self.__groupbox__()
        self.__tab__()
        self.__layout__()

    def __menubar_mso__(self):
        action_analys = QAction('분석 실행', self)
        action_analys.setShortcut('F10')
        action_analys.triggered.connect(self.Analys_mso)
        action_reset = QAction('초기화', self)
        action_reset.setShortcut('Ctrl+R')
        action_reset.triggered.connect(self.Reset)
        self.action_save_mso = QAction('엑셀로 저장', self)
        self.action_save_mso.setShortcut('Ctrl+S')
        self.action_save_mso.triggered.connect(self.Save_mso)
        self.action_save_mso.setVisible(False)
        self.menubar_mso = QMenuBar(self)
        self.menubar_mso.addAction(action_reset)
        self.menubar_mso.addAction(action_analys)
        self.menubar_mso.addAction(self.action_save_mso)

    def __menubar_ssa__(self):
        action_analys = QAction('분석 실행', self)
        action_analys.setShortcut('F10')
        action_analys.triggered.connect(self.Analys_ssa)
        action_reset = QAction('초기화', self)
        action_reset.setShortcut('Ctrl+R')
        action_reset.triggered.connect(self.Reset)
        self.action_save_ssa = QAction('엑셀로 저장', self)
        self.action_save_ssa.setShortcut('Ctrl+S')
        self.action_save_ssa.triggered.connect(self.Save_ssa)
        self.action_save_ssa.setVisible(False)
        self.menubar_ssa = QMenuBar(self)
        self.menubar_ssa.addAction(action_reset)
        self.menubar_ssa.addAction(action_analys)
        self.menubar_ssa.addAction(self.action_save_ssa)

    def __tables__(self):
        self.table_mso = MSOTable(self.db_name, self.tab_project)
        self.table_ssa = SSATable(self.db_name, self.tab_project)
        self.table_area_mso = AreaTable(self.db_name, self.tab_project)
        self.table_area_ssa = AreaTable(self.db_name, self.tab_project)
        style = "QTableWidget{color: black;}"
        self.table_mso.setStyleSheet(style)
        self.table_ssa.setStyleSheet(style)
        self.table_area_mso.setStyleSheet(style)
        self.table_area_ssa.setStyleSheet(style)

    def Reset(self):
        index = self.tab.currentIndex()
        self.method()
        self.tab.setCurrentIndex(index)

    def Analys_mso(self):
        self.checked_mso = list(set(self.table_mso.checked))
        self.checked_area = list(set(self.table_area_mso.checked))
        if not self.checked_mso:
            QMessageBox.question(self, '오류', 'MSO 논리를 선택하세요.', QMessageBox.Close)
        elif not self.checked_area:
            QMessageBox.question(self, '오류', '방화지역을 선택하세요.', QMessageBox.Close)
        else:
            self.numbers = []
            self.effects = []
            self.logics = []
            self.result_mso = []
            for row in self.checked_mso:
                number = self.table_mso.table.item(row, 2).text()
                effect = self.table_mso.table.item(row, 3).text()
                logic = self.table_mso.table.item(row, 4).text()
                self.numbers.append(number)
                self.effects.append(effect)
                self.logics.append(logic)
            self.checked_area.sort()
            self.areas_mso = []

            for row in self.checked_area:
                area = self.table_area_mso.table.item(row, 2).text()
                self.areas_mso.append(area)

            self.result_mso = []
            for logic in self.logics:
                setup = MSOSetup(self.db_name, self.areas_mso, logic)
                self.result_mso.append(setup.mso)
            self.__set_table_result_mso__()
            self.action_save_mso.setVisible(True)

    def Analys_ssa(self):
        self.checked_ssa = list(set(self.table_ssa.checked))
        self.checked_area = list(set(self.table_area_ssa.checked))
        if not self.checked_mso:
            QMessageBox.question(self, '오류', 'SSA 논리를 선택하세요.', QMessageBox.Close)
        elif not self.checked_area:
            QMessageBox.question(self, '오류', '방화지역을 선택하세요.', QMessageBox.Close)
        else:
            self.numbers = []
            self.effects = []
            self.logics = []
            self.result_ssa = []
            for row in self.checked_ssa:
                number = self.table_ssa.table.item(row, 2).text()
                effect = self.table_ssa.table.item(row, 3).text()
                logic = self.table_ssa.table.item(row, 4).text()
                self.numbers.append(number)
                self.effects.append(effect)
                self.logics.append(logic)
            self.checked_area.sort()

            self.areas_ssa = []
            for row in self.checked_area:
                area = self.table_area_ssa.table.item(row, 2).text()
                self.areas_ssa.append(area)

            self.result_ssa = []
            for logic in self.logics:
                setup = SSASetup(self.db_name, self.areas_ssa, logic)
                self.result_ssa.append(setup.ssa)
            self.__set_table_result_ssa__()
            self.action_save_ssa.setVisible(True)

    def Save_mso(self):
        dig_dirs = QFileDialog(self)
        file_path = dig_dirs.getSaveFileName(caption='엑셀로 저장', directory='', filter='*.xlsx')[0]
        if file_path != '':
            rows = self.table_result_mso.rowCount()
            cols = self.table_result_mso.columnCount()
            result_mso = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = self.table_result_mso.item(row, col).text()
                    row_data.append(item)
                result_mso.append(row_data)
            SaveResult(result_mso, self.columns_mso, 'MSO', file_path)

    def Save_ssa(self):
        dig_dirs = QFileDialog(self)
        file_path = dig_dirs.getSaveFileName(caption='엑셀로 저장', directory='', filter='*.xlsx')[0]
        if file_path != '':
            rows = self.table_result_ssa.rowCount()
            cols = self.table_result_ssa.columnCount()
            result_ssa = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    item = self.table_result_ssa.item(row, col).text()
                    row_data.append(item)
                result_ssa.append(row_data)
            SaveResult(result_ssa, self.columns_ssa, 'MSO', file_path)

    def __table_result_mso__(self):
        self.table_result_mso = QTableWidget()
        self.table_result_mso.setRowCount(0)
        self.table_result_mso.verticalHeader().setVisible(False)
        style = """
        QTableWidget{
        color: black; 
        margin-left: 9px; 
        margin-right: 9px;
        }
        QHeaderView::section
        {font-weight: bold;
        border: 2px black;}
        """
        self.table_result_mso.setStyleSheet(style)

    def __table_result_ssa__(self):
        self.table_result_ssa = QTableWidget()
        self.table_result_ssa.setRowCount(0)
        self.table_result_ssa.verticalHeader().setVisible(False)
        style = """
        QTableWidget{
        color: black; 
        margin-left: 9px; 
        margin-right: 9px;
        }
        QHeaderView::section
        {font-weight: bold;
        border: 2px black;}
        """
        self.table_result_ssa.setStyleSheet(style)

    def __set_table_result_mso__(self):
        self.table_result_mso.setRowCount(0)
        self.columns_mso = ['MSO', '영향기능'] + self.areas_mso
        self.table_result_mso.setColumnCount(len(self.columns_mso))
        self.table_result_mso.setHorizontalHeaderLabels(self.columns_mso)
        self.table_result_mso.setAlternatingRowColors(True)
        for row, name in enumerate(self.numbers):
            self.table_result_mso.insertRow(row)
            self.table_result_mso.setRowHeight(row, 50)
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_result_mso.setItem(row, 0, item)

        for row, name in enumerate(self.effects):
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEditable)
            self.table_result_mso.setItem(row, 1, item)

        for row, lst in enumerate(self.result_mso):
            for col, result in enumerate(lst):
                item = QTableWidgetItem(str(result))
                item.setFlags(Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_result_mso.setItem(row, col+2, item)
        self.table_result_mso.resizeColumnsToContents()

    def __set_table_result_ssa__(self):
        self.table_result_ssa.setRowCount(0)
        self.columns_ssa = ['SSA', '영향기능'] + self.areas_ssa
        self.table_result_ssa.setColumnCount(len(self.columns_ssa))
        self.table_result_ssa.setHorizontalHeaderLabels(self.columns_ssa)
        self.table_result_ssa.setAlternatingRowColors(True)
        for row, name in enumerate(self.numbers):
            self.table_result_ssa.insertRow(row)
            self.table_result_ssa.setRowHeight(row, 50)
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEditable)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_result_ssa.setItem(row, 0, item)

        for row, name in enumerate(self.effects):
            item = QTableWidgetItem(name)
            item.setFlags(Qt.ItemIsEditable)
            self.table_result_ssa.setItem(row, 1, item)

        for row, lst in enumerate(self.result_ssa):
            for col, result in enumerate(lst):
                item = QTableWidgetItem(str(result))
                item.setFlags(Qt.ItemIsEditable)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_result_ssa.setItem(row, col+2, item)
        self.table_result_ssa.resizeColumnsToContents()

    def __groupbox__(self):
        layout_table_mso = QHBoxLayout()
        layout_table_mso.addWidget(self.table_mso)
        layout_table_mso.addWidget(self.table_area_mso)
        layout_mso = QVBoxLayout()
        layout_mso.addWidget(self.menubar_mso)
        layout_mso.addLayout(layout_table_mso)
        layout_mso.addWidget(self.table_result_mso)
        self.groupbox_mso = QGroupBox()
        self.groupbox_mso.setLayout(layout_mso)

        layout_table_ssa = QHBoxLayout()
        layout_table_ssa.addWidget(self.table_ssa)
        layout_table_ssa.addWidget(self.table_area_ssa)
        layout_ssa = QVBoxLayout()
        layout_ssa.addWidget(self.menubar_ssa)
        layout_ssa.addLayout(layout_table_ssa)
        layout_ssa.addWidget(self.table_result_ssa)
        self.groupbox_ssa = QGroupBox()
        self.groupbox_ssa.setLayout(layout_ssa)

    def __tab__(self):
        idx = self.__connect_tabidx__.Return_AnalysTab()
        self.tab = QTabWidget()
        self.tab.addTab(self.groupbox_mso, 'MSO')
        self.tab.addTab(self.groupbox_ssa, 'SSA')
        self.tab.setCurrentIndex(idx)
        self.tab.tabBarClicked.connect(self.SaveTabIndex)

    def SaveTabIndex(self, idx):
        self.__connect_tabidx__.Update_AnalysTab(idx)

    def __layout__(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tab)
        self.setLayout(layout)