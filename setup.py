from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys

# pyinstaller -w --icon=icon.ico -p _dllFiles setup.py
__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class SplashScreen(QSplashScreen):
    def __init__(self):
        QSplashScreen.__init__(self)
        self.setPixmap(QPixmap('logo.png').scaledToWidth(800))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.mousePressEvent = self.MousePressEvent

    def MousePressEvent(self, event):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splashscreen = SplashScreen()
    splashscreen.show()
    from Component.Windows import Windows
    from Connector.TabSetting import TabSetting
    win = Windows()
    connector_tabidx = TabSetting()
    connector_tabidx.Update_LogicTab(0)
    connector_tabidx.Update_AnalysTab(0)
    win.show()
    splashscreen.finish(win)
    app.exec_()