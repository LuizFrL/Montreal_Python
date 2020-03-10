from Banco.Conect import Conect


class MailAuditDAO(Conect):

    def __init__(self):
        Conect.__init__(self, database='MAIL_AUDIT', trusted_connection=True)

    def insert_endereco_emails(self, itens: tuple):
        query = f"""
        INSERT INTO dbo.endereco_emails
        VALUES  {str(itens)}
        """
        return self._exec_query(query)

    def insert_mensagens(self, itens: tuple):
        query = f"""
        INSERT INTO dbo.mensagens
        VALUES  {str(itens)}
        """
        return self._exec_query(query)

    def insert_anexos(self, itens: tuple):
        pass
