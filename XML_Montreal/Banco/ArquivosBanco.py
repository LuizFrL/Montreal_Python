import pyodbc


class ArquivosBanco(object):

    def __init__(self):
        self.driver = '{SQL Server Native Client 11.0}'
        self.server = '172.31.0.6'
        self.database = 'montreal'
        self.usuario = 'nfe'
        self.pasword = 'nfe2019'
        self.conexao = pyodbc.connect(f'DRIVER={self.driver};'
                                      f'SERVER={self.server};'
                                      f'DATABASE={self.database};'
                                      f'UID={self.usuario};'
                                      f'PWD={self.pasword}')
        self.cursor = self. conexao.cursor()

    def informacoes_tabela(self):
        print('Coletando Linhas da Tabela.')
        linhas = self.cursor.execute("""select * from dbo.nfe_NotasResult""")
        return [linha for linha in linhas]

    def colunas_tabela(self):
        print('Coletando Colunas da Tabela.')
        colunas = self.cursor.execute("""EXECUTE sp_columns nfe_NotasResult""")
        return [coluna[3] for coluna in colunas]

    def arquivos_banco(self):
        print('Montando Informações.')
        colunas = self.colunas_tabela()
        linhas = self.informacoes_tabela()
        return self.__montar_estrutura(colunas, linhas)

    def __montar_estrutura(self, colunas, linhas):
        arquivos = []
        for linha in linhas:
            arq = {}
            for index, coluna in enumerate(colunas):
                arq[coluna] = linha[index]
            arquivos.append(arq)
        return arquivos

    def remover_arquivos_erro(self):
        print('Removendo arquivos com erro...')
        self.cursor.execute("""
DELETE
from        dbo.nfe_NotasResult
where       autorizacao_cStat not in (100, 103)
""")
        self.conexao.commit()
        print('Arquivos deletados com sucesso.')

    def arquivos(self):
        return [item['arquivoOriginal'] for item in self.arquivos_banco()]

    def format_query(self, valores:'Dicionario com keys=colunas_banco'):
        query = f"""
INSERT INTO dbo.nfe_NotasResult {str(tuple(valores.keys())).replace("'", '')}
VALUES {str(tuple(str(item).replace("'", '') for item in valores.values()))}"""
        return query

    def adicionar_banco(self, coluna_valores, ver_query=False):
        query = self.format_query(coluna_valores)
        print(query) if ver_query else None

        try:
            self.cursor.execute(query)
            self.conexao.commit()
            situacao = 'Nota Fiscal adicionada.'
        except Exception as err:
            situacao = err
        return situacao
