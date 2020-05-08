from PyQt5.QtWidgets import QTabWidget
from Component.Projects.AreaTab import AreaTab
from Component.Projects.EquipTab import EquipTab
from Component.Projects.CableTab import CableTab
from Component.Projects.LogicTap import LogicTab
from Component.Projects.AnalysTab import AnalysTab

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Project(QTabWidget):
    def __init__(self, db_name, method):
        QTabWidget.__init__(self)
        self.db_name = db_name
        self.addTab(AreaTab(db_name, self, method), '방화지역')
        self.addTab(EquipTab(db_name, self, method), '기기')
        self.addTab(CableTab(db_name, self, method), '케이블')
        self.addTab(LogicTab(db_name, self, method), '논리')
        self.addTab(AnalysTab(db_name, self, method), '분석')