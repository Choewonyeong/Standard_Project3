import sqlite3 as sq
import pandas as pd

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class ConnectorEquip:
    def __init__(self, db_name):
        self.path = f"Data/{db_name}/기기정보.db"

    def Delete_Table(self):
        pass

    def Insert(self, number):
        try:
            sql = f"""
            INSERT INTO `기기정보`(`순번`)
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
            UPDATE `기기정보` 
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
            DELETE FROM `기기정보`
            WHERE `순번`='{number}';"""
            conn = sq.connect(self.path)
            conn.execute(sql)
            conn.commit()
            conn.close()
        except:
            pass


class ReturnEquip:
    def __init__(self, db_name):
        self.path = f"Data/{db_name}/기기정보.db"

    def Columns(self):
        try:
            sql = """
            SELECT * FROM `기기정보`;
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
            SELECT * FROM `기기정보`;
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

    def Equipments(self):
        try:
            sql = """
            SELECT `기기번호` FROM `기기정보`;
            """
            conn = sq.connect(self.path)
            curs = conn.cursor()
            curs.execute(sql)
            equipments = [equipment[0] for equipment in curs.fetchall()]
            curs.close()
            conn.close()
            return equipments
        except:
            return []
