import pandas as pd
import sqlite3 as sq
import os

__author__ = "Wonyeong Choe <choewy@stdte.co.kr>"


class Export:
    def __init__(self, db_name, file_path, parent=None):
        self.db_name = db_name
        self.file_path = file_path
        self.parent = parent
        self.__setup__()

    def __setup__(self):
        db_path = f"Data/"
        writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
        file_names = os.listdir(db_path+self.db_name)
        file_names = [file_name[:len(file_name)-3] for file_name in file_names]
        for file_name in file_names:
            conn = sq.connect(f"{db_path}/{self.db_name}/{file_name}.db")
            if file_name in ['논리정보(MSO)', '논리정보(SSA)']:
                table = '논리정보'
            else:
                table = file_name
            sql = f"SELECT * FROM `{table}`;"
            df = pd.read_sql(sql, conn)
            df.to_excel(writer, sheet_name=file_name, index=False)
            conn.close()
        writer.close()