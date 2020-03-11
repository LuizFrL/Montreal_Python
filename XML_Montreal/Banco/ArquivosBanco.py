from Banco.Conect import Conect


class ArquivosBanco(Conect):

    def __init__(self):
        super().__init__(usuario='nfe', pasword='nfe2019', server='172.31.0.6')

    def arquivos_banco(self):
        return self._exec_query("""select * from dbo.nfe_NotasResult""")

    def remover_arquivos_erro(self):
        print('Removendo arquivos com erro...')
        self.cursor.execute("""
DELETE
from    dbo.nfe_NotasResult
WHERE   autorizacao_cStat not in (100)
""")
        print(f'Total de { self.cursor.rowcount } linhas afetadas.')
        self.conexao.commit()

        print('Arquivos deletados com sucesso.')

    def arquivos(self):
        return self._exec_query("""select arquivoOriginal from dbo.nfe_NotasResult""")

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
            situacao = err.__str__()
        return situacao

