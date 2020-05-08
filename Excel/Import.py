import openpyxl as ox
import pandas as pd
import sqlite3 as sq

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Import:
    def __init__(self, db_name, file_name, parent=None):
        self.db_name = db_name
        self.file_name = file_name
        self.parent = parent
        self.__setup__()

    def __setup__(self):
        workbook = ox.load_workbook(self.file_name)
        worksheets = workbook.sheetnames
        for sheet in worksheets:
            path = f"Data/{self.db_name}/{sheet}.db"
            conn = sq.connect(path)
            df = pd.read_excel(self.file_name, sheet)
            df.fillna('')
            if sheet in ['논리정보(MSO)', '논리정보(SSA)']:
                table = '논리정보'
            else:
                table = sheet
            df.to_sql(table, conn, index=False)
            conn.commit()
            sql = f"SELECT * FROM `{table}`;"
            curs = conn.cursor()
            query = curs.execute(sql)
            columns = [column[0] for column in query.description]
            for column in columns:
                sql = f"UPDATE `{table}` SET `{column}`='' WHERE `{column}` IS NULL;"
                query.execute(sql)
                conn.commit()
            curs.close()
            conn.close()
