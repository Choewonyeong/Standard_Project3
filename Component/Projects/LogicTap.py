from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTabWidget
from Component.Projects.Logics.MSOTable import MSOTable
from Component.Projects.Logics.SSATable import SSATable
from Connector.TabSetting import TabSetting

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class LogicTab(QWidget):
    def __init__(self, db_name, tab_project, method):
        QWidget.__init__(self)
        self.tab_project = tab_project
        self.method = method
        self.db_name = db_name
        self.__connect_tabidx__ = TabSetting()
        self.__component__()

    def __component__(self):
        self.__table__()
        self.__tab__()
        self.__layout__()

    def __table__(self):
        self.table_mso = MSOTable(self.db_name, self.tab_project, self.method)
        self.table_ssa = SSATable(self.db_name, self.tab_project, self.method)

    def __tab__(self):
        self.tab = QTabWidget()
        idx = self.__connect_tabidx__.Return_LogicTab()
        self.tab.addTab(self.table_mso, 'MSO')
        self.tab.addTab(self.table_ssa, 'SSA')
        self.tab.setCurrentIndex(idx)
        self.tab.tabBarClicked.connect(self.SaveTabIndex)

    def SaveTabIndex(self, idx):
        self.__connect_tabidx__.Update_LogicTab(idx)

    def __layout__(self):
        layout = QHBoxLayout()
        layout.addWidget(self.tab)
        self.setLayout(layout)