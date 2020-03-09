import pyodbc, pandas as pd


class Conect(object):
    def __init__(self):
        self.driver = '{SQL Server Native Client 11.0}'
        self.server = 'cltsql01'
        self.database = 'montreal'
        self.usuario = 'web_usr'
        self.pasword = 'Ch4rm8s8'
        self.conexao = pyodbc.connect(f'DRIVER={self.driver};'
                                      f'SERVER={self.server};'
                                      f'DATABASE={self.database};'
                                      f'UID={self.usuario};'
                                      f'PWD={self.pasword}', autocommit=True)
        self.cursor = self.conexao.cursor()

    def _exec_query(self, query):
        print(query)
        return pd.read_sql(query, self.conexao)


if __name__ == '__main__':
    test_connection = Conect()
