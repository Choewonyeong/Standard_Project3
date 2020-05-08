import pandas as pd
import sqlite3 as sq
import os


class SaveResult:
    def __init__(self, lst, columns, option, file_path, parent=None):
        self.dataframe = pd.DataFrame(lst, columns=columns)
        self.option = option
        self.file_path = file_path
        self.parent = parent
        self.__setup__()

    def __setup__(self):
        writer = pd.ExcelWriter(self.file_path, engine='xlsxwriter')
        self.dataframe.to_excel(writer, sheet_name=self.option, index=False)
        writer.close()