import sqlite3 as sq

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class TabSetting:
    def __init__(self):
        self.path = 'Setting/Tab.db'

    def Update_LogicTab(self, index):
        try:
            sql = f"UPDATE `Tab` SET `논리정보`='{index}';"
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
        except:
            pass

    def Update_AnalysTab(self, index):
        try:
            sql = f"UPDATE `Tab` SET `분석`='{index}';"
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
        except:
            pass

    def Return_LogicTab(self):
        try:
            sql = "SELECT `논리정보` FROM `Tab`;"
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            idx = int(curs.fetchone()[0])
            curs.close()
            conn.close()
            return idx
        except:
            return 0

    def Return_AnalysTab(self):
        try:
            sql = "SELECT `분석` FROM `Tab`;"
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            idx = int(curs.fetchone()[0])
            curs.close()
            conn.close()
            return idx
        except:
            return 0
