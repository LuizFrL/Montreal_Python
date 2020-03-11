import pyodbc, pandas as pd


class Conect(object):

    def __init__(self, driver='{SQL Server Native Client 11.0}',
                 server='cltsql01',
                 database='montreal',
                 usuario='0',
                 pasword='0', trusted_connection=False):
        self.driver = driver
        self.server = server
        self.database = database
        self.usuario = usuario
        self.pasword = pasword
        connect_inf = f'''DRIVER={self.driver};
SERVER={self.server};
DATABASE={self.database};'''
        if trusted_connection:
            connect_inf += '\nTrusted_Connection=yes;'
        else:
            connect_inf += f'\nUID={self.usuario};\nPWD={self.pasword};'
        self.conexao = pyodbc.connect(connect_inf, autocommit=True)
        self.cursor = self.conexao.cursor()

    def _exec_select_query(self, query) -> pd:
        print(query)
        return pd.read_sql(query, self.conexao)

    def _exec_insert_query(self, query: str):
        print(query)
        self.cursor.execute(query)
        self.conexao.commit()


if __name__ == '__main__':
    test_connection = Conect()
