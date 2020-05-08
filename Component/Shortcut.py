from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Shortcut(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.__setting__()
        self.__component__()

    def __setting__(self):
        style = "QWidget{background-color: white;}"
        self.setStyleSheet(style)

    def __component__(self):
        self.__table_main__()
        self.__table_tab__()
        self.__layout__()

    def __table_main__(self):
        columns = ['   기능   ', '   단축키   ', '설명']
        option_main = ['프로그램 종료', '새 프로젝트 생성', '프로젝트 관리', '업로드', '다운로드']
        shortcut_main = ['Ctrl + Q', 'Ctrl + N', 'Ctrl + M', 'F5', 'Ctrl + I', 'Ctrl + E']
        summary_main = ['프로그램을 종료합니다.',
                        '새로운 프로젝트를 생성하기 위한 창을 엽니다.\n프로젝트 명을 입력받습니다.',
                        '프로젝트를 관리하기 위한 창을 엽니다.\n프로젝트를 삭제할 수 있습니다.',
                        '엑셀 파일을 불러옵니다.\n[분석]탭을 제외한 모든 탭의 데이터베이스를 재구성합니다.',
                        '[분석]탭을 제외한 모든 탭의 데이터를 엑셀 파일로 내보냅니다.']
        style = "QTableWidget{border: 0px; color: black;} QHeaderView::section {font-weight: bold; border: 2px black;}"
        self.table_main = QTableWidget()
        self.table_main.setStyleSheet(style)
        self.table_main.setRowCount(0)
        self.table_main.setColumnCount(len(columns))
        self.table_main.setHorizontalHeaderLabels(columns)
        self.table_main.setAlternatingRowColors(True)
        for row, [option, shortcut, summary] in enumerate(zip(option_main, shortcut_main, summary_main)):
            self.table_main.insertRow(row)
            self.table_main.setRowHeight(row, 70)
            item_option = QTableWidgetItem(str(option))
            item_option.setTextAlignment(Qt.AlignCenter)
            item_option.setFlags(Qt.ItemIsEditable)
            self.table_main.setItem(row, 0, item_option)

            item_shortcut = QTableWidgetItem(str(shortcut))
            item_shortcut.setTextAlignment(Qt.AlignCenter)
            item_shortcut.setFlags(Qt.ItemIsEditable)
            self.table_main.setItem(row, 1, item_shortcut)

            item_summary = QTableWidgetItem(str(summary))
            item_summary.setFlags(Qt.ItemIsEditable)
            self.table_main.setItem(row, 2, item_summary)

            self.table_main.resizeColumnsToContents()
        self.table_main.verticalHeader().setVisible(False)
        self.table_main.horizontalHeader().setStretchLastSection(True)
        self.table_main.horizontalScrollBar().setVisible(False)

    def __table_tab__(self):
        columns = ['   기능   ', '   단축키   ', '설명']
        option_tab = ['추가', '삭제', '저장', '엑셀로 저장', '초기화', '분석실행']
        shortcut_tab = ['Alt + 1', 'Alt + 2', 'Ctrl + S', 'Ctrl + S', 'Ctrl + R', 'F10']
        summary_tab = ['행을 추가합니다.\n새 정보를 입력할 수 있습니다.',
                       '선택한 항목을 삭제합니다.\n삭제된 정보는 데이터베이스에서도 즉시 삭제됩니다.',
                       '수정된 데이터를 저장합니다.\n다른 탭의 저장되지 않은 정보는 삭제됩니다.\n각 탭의 정보를 수정한 후에는 반드시 저장하시기 바랍니다.',
                       '분석 시 선택한 항목 및 결과를 초기화합니다.\n※ [분석]탭에만 존재하는 기능입니다.',
                       '선택한 항목을 반영하여 분석을 실행합니다.\n※ [분석]탭에만 존재하는 기능입니다.',
                       '분석 결과를 엑셀로 저장합니다.\n분석을 실행한 후 버튼이 생기도록 되어있습니다.\n※ [분석]탭에만 존재하는 기능입니다.']
        style = "QTableWidget{border: 0px; color: black;} QHeaderView::section {font-weight: bold; border: 2px black;}"
        self.table_tab = QTableWidget()
        self.table_tab.setStyleSheet(style)
        self.table_tab.setRowCount(0)
        self.table_tab.setColumnCount(len(columns))
        self.table_tab.setHorizontalHeaderLabels(columns)
        self.table_tab.setAlternatingRowColors(True)
        for row, [option, shortcut, summary] in enumerate(zip(option_tab, shortcut_tab, summary_tab)):
            self.table_tab.insertRow(row)
            self.table_tab.setRowHeight(row, 70)
            item_option = QTableWidgetItem(str(option))
            item_option.setTextAlignment(Qt.AlignCenter)
            item_option.setFlags(Qt.ItemIsEditable)
            self.table_tab.setItem(row, 0, item_option)

            item_shortcut = QTableWidgetItem(str(shortcut))
            item_shortcut.setTextAlignment(Qt.AlignCenter)
            item_shortcut.setFlags(Qt.ItemIsEditable)
            self.table_tab.setItem(row, 1, item_shortcut)

            item_summary = QTableWidgetItem(str(summary))
            item_summary.setFlags(Qt.ItemIsEditable)
            self.table_tab.setItem(row, 2, item_summary)

            self.table_tab.resizeColumnsToContents()
        self.table_tab.verticalHeader().setVisible(False)
        self.table_tab.horizontalHeader().setStretchLastSection(True)
        self.table_tab.horizontalScrollBar().setVisible(False)

    def __layout__(self):
        layout_table_main = QVBoxLayout()
        layout_table_main.addWidget(QLabel('※ 메인 단축키'), 0)
        layout_table_main.addWidget(self.table_main)
        layout_table_tab = QVBoxLayout()
        layout_table_tab.addWidget(QLabel('※ 탭 단축키'), 0)
        layout_table_tab.addWidget(self.table_tab)
        layout = QVBoxLayout()
        layout.addLayout(layout_table_main)
        layout.addLayout(layout_table_tab)
        self.setLayout(layout)