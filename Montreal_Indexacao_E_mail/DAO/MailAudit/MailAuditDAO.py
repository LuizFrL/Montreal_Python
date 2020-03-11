import time

from Banco.Conect import Conect


class MailAuditDAO(Conect):

    def __init__(self):
        Conect.__init__(self, database='MAIL_AUDIT', trusted_connection=True)

    def insert_endereco_emails(self, itens: tuple):
        query = f"""
        INSERT INTO dbo.endereco_emails
        VALUES  {str(itens)}
        """
        self._exec_insert_query(query)

    def insert_mensagens(self, itens: tuple):
        query = f"""
        INSERT INTO dbo.mensagens
        VALUES  {str(itens)}
        """
        self._exec_insert_query(query)

    def insert_anexos(self, itens: str):
        query = f"""
        INSERT INTO dbo.anexos
        VALUES  {itens}"""
        self._exec_insert_query(query)


if __name__ == '__main__':
    teste_connection = MailAuditDAO()
