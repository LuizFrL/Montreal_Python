import time

from Banco.Conect import Conect


class MailAuditDAO(Conect):

    def __init__(self):
        Conect.__init__(self, database='MAIL_AUDIT', trusted_connection=True)

    def insert_endereco_emails(self, itens: str):
        query = f"""
        INSERT INTO dbo.endereco_emails
        VALUES  {itens}
        """
        self._exec_insert_query(query)

    def insert_mensagens(self, itens: str):
        query = f"""
        INSERT INTO dbo.mensagens
        VALUES  {itens}
        """
        self._exec_insert_query(query)

    def insert_anexos(self, itens: str):
        query = f"""
        INSERT INTO dbo.anexos ( id_anexo, md5, filename, content_type, tamanho )
        VALUES  {itens}"""
        self._exec_insert_query(query)


if __name__ == '__main__':
    teste_connection = MailAuditDAO()
