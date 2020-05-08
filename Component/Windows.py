from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QAction, QMenu, QMenuBar, QLineEdit
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtWidgets import QMessageBox, QComboBox, QTabWidget, QFileDialog
from PyQt5.QtWidgets import QFormLayout, QPushButton, QVBoxLayout, QHBoxLayout
from Component.Shortcut import Shortcut
from Component.Materials import Checkbox
from Component.Materials import CheckboxItem
from Component.Projects.AreaTab import AreaTab
from Component.Projects.CableTab import CableTab
from Component.Projects.EquipTab import EquipTab
from Component.Projects.LogicTap import LogicTab
from Component.Projects.AnalysTab import AnalysTab
from Component.Project import Project
from Excel.Import import Import
from Excel.Export import Export
import shutil
import os

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Windows(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.dirs = ['']+os.listdir('Data')
        self.dirs.remove('Origin')
        self.db_name = ''
        self.__setting__()
        self.__component__()

    def __setting__(self):
        self.setWindowTitle('원전 MSO, SSA 분석 프로그램')
        self.setMinimumWidth(800)
        self.setMinimumHeight(800)
        self.geometry().center()
        self.showMaximized()
        self.setWindowIcon(QIcon('icon.ico'))

    def __component__(self):
        self.__menubar__()
        self.__combobox__()
        self.__pushbutton__()
        self.__tab__()
        self.__layout__()

    def __menubar__(self):
        action_version = QAction('프로그램 정보', self)
        self.action_shortcut = QAction('단축키 정보', self)
        action_exit = QAction('닫기', self)
        action_exit.setShortcut('Ctrl+Q')
        action_version.triggered.connect(self.Version)
        self.action_shortcut.triggered.connect(self.Shortcut)
        action_exit.triggered.connect(self.Exit)
        menu_main = QMenu('메뉴', self)
        menu_main.addAction(action_version)
        menu_main.addAction(self.action_shortcut)
        menu_main.addSeparator()
        menu_main.addAction(action_exit)
        action_new = QAction('새 프로젝트', self)
        action_new.setShortcut('Ctrl+N')
        action_admin = QAction('프로젝트 관리', self)
        action_admin.setShortcut('Ctrl+M')
        action_refresh = QAction('새로고침', self)
        action_refresh.setShortcut('F5')
        action_new.triggered.connect(self.New)
        action_admin.triggered.connect(self.Admin)
        action_refresh.triggered.connect(self.Refresh)
        menu_project = QMenu('프로젝트', self)
        menu_project.addAction(action_new)
        menu_project.addAction(action_admin)
        menu_project.addAction(action_refresh)
        self.menubar = QMenuBar(self)
        self.menubar.addMenu(menu_main)
        self.menubar.addMenu(menu_project)

    def New(self):
        self.lineedit_project = QLineEdit()
        self.button_close = QPushButton('닫기')
        self.button_create = QPushButton('생성')
        self.button_create.setDefault(True)
        self.button_close.clicked.connect(self.Close)
        self.button_create.clicked.connect(self.Create)
        layout_form = QFormLayout()
        layout_form.addRow('프로젝트 명', self.lineedit_project)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_close)
        layout_buttons.addWidget(self.button_create)
        layout = QVBoxLayout()
        layout.addLayout(layout_form)
        layout.addLayout(layout_buttons)
        self.dig = QDialog(self)
        self.dig.setLayout(layout)
        self.dig.setFixedWidth(300)
        self.dig.setFixedHeight(100)
        self.dig.setWindowTitle('새 프로젝트 생성')
        self.dig.exec_()

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

    def Admin(self):
        self.checked = []
        dirs = ['']+os.listdir('Data')
        dirs.remove('Origin')
        action_close = QAction('닫기')
        action_close.triggered.connect(self.CloseProject)
        action_delete = QAction('삭제')
        action_delete.setShortcut('Alt+2')
        action_delete.triggered.connect(self.DeleteProject)
        menubar = QMenuBar()
        menubar.addAction(action_close)
        menubar.addAction(action_delete)
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(len(['선택', '프로젝트명']))
        self.table.setHorizontalHeaderLabels(['선택', '프로젝트명'])
        style = "QTableWidget{color: black;}"
        self.table.setStyleSheet(style)
        for row, project in enumerate(dirs):
            self.table.insertRow(row)
            self.table.setRowHeight(row, 50)
            self.__checkbox__(self.table, row, 0)
            item = QTableWidgetItem(project)
            item.setFlags(Qt.ItemIsEditable)
            self.table.setItem(row, 1, item)
        self.table.resizeColumnsToContents()
        self.table.hideRow(0)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout = QVBoxLayout()
        layout.addWidget(menubar)
        layout.addWidget(self.table)
        self.dig_project = QDialog(self)
        self.dig_project.setLayout(layout)
        self.dig_project.setWindowTitle('프로젝트 관리')
        self.dig_project.setFixedWidth(400)
        self.dig_project.setFixedHeight(800)
        self.dig_project.exec_()

    def CloseProject(self):
        self.dig_project.close()

    def DeleteProject(self):
        self.checked.sort(reverse=True)
        for row in self.checked:
            project = self.table.item(row, 1).text()
            index = self.dirs.index(project)
            current = f"Data/{project}"
            shutil.rmtree(current)
            self.combobox_project.removeItem(index)
            self.dirs.remove(project)
            self.table.removeRow(row)
        self.checked.clear()

    def Refresh(self):
        index = self.project.currentIndex()
        self.project.clear()
        self.project.addTab(AreaTab(self.db_name, self, self.Refresh), '방화지역')
        self.project.addTab(EquipTab(self.db_name, self, self.Refresh), '기기')
        self.project.addTab(CableTab(self.db_name, self, self.Refresh), '케이블')
        self.project.addTab(LogicTab(self.db_name, self, self.Refresh), '논리')
        self.project.addTab(AnalysTab(self.db_name, self, self.Refresh), '분석')
        self.project.setCurrentIndex(index)

    def Version(self):
        pixmap = QPixmap('logo.png').scaledToWidth(300)
        label_logo = QLabel()
        label_logo.setPixmap(pixmap)
        label_logo.setAlignment(Qt.AlignCenter)
        label_title = QLabel('<h3>원전 MSO, SSA 분석 프로그램 V1.0</h3>')
        label_title.setAlignment(Qt.AlignCenter)
        layout_head = QVBoxLayout()
        layout_head.addWidget(QLabel('소    속 :'))
        layout_head.addWidget(QLabel('개 발 자 :'))
        layout_head.addWidget(QLabel('제 작 일 :'))
        layout_head.addWidget(QLabel('개    요 :'))
        layout_head.addWidget(QLabel(''))
        layout_content = QVBoxLayout()
        layout_content.addWidget(QLabel('(주)스탠더드시험연구소'))
        layout_content.addWidget(QLabel('최원영'))
        layout_content.addWidget(QLabel('2019-06-10'))
        layout_content.addWidget(QLabel('본 프로그램은 (주)스탠더드시험연구소에서 자체적으로 개발한'))
        layout_content.addWidget(QLabel('원전 다중오동작(MSO), 안전정지(SSA) 분석을 위한 프로그램입니다.'))
        layout_info = QHBoxLayout()
        layout_info.addLayout(layout_head)
        layout_info.addLayout(layout_content)
        layout = QVBoxLayout()
        layout.addWidget(label_title)
        layout.addWidget(QLabel(''))
        layout.addLayout(layout_info)
        layout.addWidget(QLabel(''))
        layout.addWidget(label_logo)
        self.dig_version = QDialog(self)
        self.dig_version.setStyleSheet('QDialog{background: white;}')
        self.dig_version.setWindowTitle('프로그램 정보')
        self.dig_version.setLayout(layout)
        self.dig_version.setFixedWidth(460)
        self.dig_version.setFixedHeight(280)
        self.dig_version.exec_()

    def Shortcut(self):
        idx = self.tab.count()
        self.tab.addTab(Shortcut(), '단축키 정보')
        self.tab.setCurrentIndex(idx)
        self.action_shortcut.setEnabled(False)

    def Exit(self):
        self.close()

    def Create(self):
        db_name = self.lineedit_project.text()
        if db_name == '':
            QMessageBox.question(self, '오류', '프로젝트 이름을 입력하세요.', QMessageBox.Close)
        elif os.path.isdir(f"Data/{db_name}"):
            QMessageBox.question(self, '오류', '이미 존재하는 프로젝트입니다.', QMessageBox.Close)
        elif db_name != '':
            self.dirs.append(db_name)
            origin = os.listdir("Data/Origin")
            os.makedirs(f"Data/{db_name}")
            for index, db in enumerate(origin):
                origin_db = f"Data/Origin/{db}"
                new_db = f"Data/{db_name}/{db}"
                shutil.copy(origin_db, new_db)
            self.dig.close()
            self.combobox_project.addItems([f'{db_name}'])

    def Close(self):
        self.dig.close()

    def __combobox__(self):
        self.combobox_project = QComboBox()
        self.combobox_project.addItems(self.dirs)

    def __pushbutton__(self):
        self.button_project = QPushButton('열기')
        self.button_project.clicked.connect(self.Open)
        self.button_import = QPushButton('업로드')
        self.button_import.clicked.connect(self.Import)
        self.button_import.setVisible(False)
        self.button_export = QPushButton('다운로드')
        self.button_export.clicked.connect(self.Export)
        self.button_export.setVisible(False)

    def Open(self):
        self.db_name = self.combobox_project.currentText()
        count = self.tab.count()
        tab_bars = []
        if count != 0:
            for idx in range(count):
                text = self.tab.tabText(idx)
                tab_bars.append(text)
        if self.db_name == '':
            self.button_import.setVisible(False)
            self.button_export.setVisible(False)

        elif self.db_name != '' and self.db_name not in tab_bars:
            self.project = Project(self.db_name, self.Refresh)
            self.tab.addTab(self.project, self.db_name)
            self.tab.setCurrentIndex(self.tab.currentIndex()+1)
            self.button_import.setVisible(True)
            self.button_export.setVisible(True)
            self.button_import.setShortcut('Ctrl+I')
            self.button_export.setShortcut('Ctrl+E')

    def Import(self):
        dig_file = QFileDialog(self)
        file_name = dig_file.getOpenFileName(self, caption='엑셀 파일 업로드', directory='', filter='*.xlsx')[0]
        if file_name != '':
            try:
                db_path = f"Data/{self.db_name}"
                shutil.rmtree(db_path)
                os.makedirs(db_path)
                Import(self.db_name, file_name)
                self.Refresh()
            except:
                QMessageBox.question(self, '오류', '업로드에 실패하였습니다.\n엑셀 파일의 양식을 확인하세요.', QMessageBox.Close)

    def Export(self):
        dig_dirs = QFileDialog(self)
        file_path = dig_dirs.getSaveFileName(caption='엑셀 파일 다운로드', directory='', filter='*.xlsx')[0]
        if file_path != '':
            Export(self.db_name, file_path)
            self.Refresh()
            self.__success_export__(file_path)

    def __success_export__(self, file_path):
        label_text = QLabel('다운로드가 완료되었습니다.\n')
        label_text.setAlignment(Qt.AlignCenter)
        self.file_path = file_path
        self.button_ignore = QPushButton('닫기')
        self.button_open = QPushButton('열기')
        self.button_ignore.clicked.connect(self.Ignore_ExcelFile)
        self.button_open.clicked.connect(self.Open_ExcelFile)
        layout_button = QHBoxLayout()
        layout_button.addWidget(self.button_ignore)
        layout_button.addWidget(self.button_open)
        layout = QVBoxLayout()
        layout.addWidget(label_text)
        layout.addLayout(layout_button)
        self.dig_export = QDialog(self)
        self.dig_export.setLayout(layout)
        self.dig_export.setWindowTitle('알림')
        style = "QDialog{background-color: white;}"
        self.dig_export.setFixedWidth(300)
        self.dig_export.setFixedHeight(150)
        self.dig_export.setStyleSheet(style)
        self.dig_export.show()

    def Ignore_ExcelFile(self):
        self.dig_export.close()

    def Open_ExcelFile(self):
        os.system(f"start excel.exe {self.file_path}")
        self.dig_export.close()

    def __tab__(self):
        self.tab = QTabWidget()
        self.tab.setMovable(True)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.CloseTab)

    def CloseTab(self, index):
        self.tab.removeTab(index)
        tab_name = self.tab.tabText(index)
        if tab_name == '단축키 정보':
            self.action_shortcut.setEnabled(True)

    def __layout__(self):
        layout_project = QHBoxLayout()
        layout_project.addWidget(QLabel('  프로젝트 선택'))
        layout_project.addWidget(self.combobox_project, 5)
        layout_project.addWidget(self.button_project, 0)
        layout_excelfile = QHBoxLayout()
        layout_excelfile.addWidget(QLabel(''), 10)
        layout_excelfile.addWidget(self.button_import, 1)
        layout_excelfile.addWidget(self.button_export, 1)
        layout_top = QHBoxLayout()
        layout_top.addLayout(layout_project, 5)
        layout_top.addLayout(layout_excelfile, 5)
        layout = QVBoxLayout()
        layout.addWidget(self.menubar, 0)
        layout.addLayout(layout_top, 0)
        layout.addWidget(self.tab, 10)
        self.setLayout(layout)






