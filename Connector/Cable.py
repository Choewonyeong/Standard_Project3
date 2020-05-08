import sqlite3 as sq
import pandas as pd

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class ConnectorCable:
    def __init__(self, db_name):
        self.path = f"Data/{db_name}/케이블정보.db"

    def Delete_Table(self):
        pass

    def Insert(self, number):
        try:
            sql = f"""
            INSERT INTO `케이블정보`(`순번`)
            VALUES('{number}');"""
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            conn.commit()
            curs.close()
            conn.close()
        except:
            pass

    def Update(self, number, column, data):
        try:
            sql = f"""
            UPDATE `케이블정보`
            SET `{column}`='{data}'
            WHERE `순번`='{number}'"""
            conn = sq.connect(self.path)
            conn.execute(sql)
            conn.commit()
            conn.close()
        except:
            pass

    def Delete(self, number):
        try:
            sql = f"""
            DELETE FROM `케이블정보`
            WHERE `순번`='{number}';"""
            conn = sq.connect(self.path)
            conn.execute(sql)
            conn.commit()
            conn.close()
        except:
            pass


class ReturnCable:
    def __init__(self, db_name):
        self.path = f"Data/{db_name}/케이블정보.db"

    def Columns(self):
        try:
            sql = """
            SELECT * FROM `케이블정보`;
            """
            conn = sq.connect(self.path)
            curs = conn.cursor()
            query = curs.execute(sql)
            columns = [column[0] for column in query.description]
            curs.close()
            conn.close()
            return columns
        except:
            return []

    def Dataframe(self):
        try:
            sql = """
            SELECT * FROM `케이블정보`;
            """
            conn = sq.connect(self.path)
            curs = conn.cursor()
            query = curs.execute(sql)
            columns = [column[0] for column in query.description]
            df = pd.DataFrame.from_records(data=query.fetchall(), columns=columns)
            curs.close()
            conn.close()
            return df
        except:
            return None

    def Route(self, equip):
        route = []
        for number in range(1, 21):
            route += self.__route__(number, equip)
        return route

    def __route__(self, number, equip):
        try:
            sql = f"""
            SELECT `경로{number}` FROM `케이블정보` 
            WHERE `해당기기`='{equip}';"""
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            route = [area[0] for area in curs.fetchall()]
            curs.close()
            conn.close()
            return route
        except:
            return []