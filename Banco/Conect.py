import pyodbc, pandas as pd


class Conect(object):
    def __init__(self, driver='{SQL Server Native Client 11.0}',
                 server='cltsql01',
                 database='montreal',
                 usuario='web_usr',
                 pasword='Ch4rm8s8'):

        self.driver = driver
        self.server = server
        self.database = database
        self.usuario = usuario
        self.pasword = pasword
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
