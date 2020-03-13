import time

from Banco.Conect import Conect


class MailAuditDAO(Conect):

    def __init__(self):
        Conect.__init__(self, database='MAIL_AUDIT', usuario='python', pasword='pluiz123')

    def _insert_endereco_emails(self, itens: str):
        query = f"""
        INSERT INTO dbo.endereco_emails (id_email, nome, email)
        VALUES  {itens}
        """
        self._exec_insert_query(query)

    def _insert_mensagens(self, itens: str):
        query = f"""
        INSERT INTO dbo.mensagens
        VALUES  {itens}
        """
        self._exec_insert_query(query)

    def _insert_anexos(self, itens: str):
        query = f"""
        INSERT INTO dbo.anexos ( id_anexo, md5, filename, content_type, tamanho )
        VALUES  {itens}"""
        self._exec_insert_query(query)

    def _insert_mensagem_to(self, itens: str):
        query = f"""
        INSERT INTO dbo.mensagem_to
        VALUES {itens}
        """
        return self._exec_insert_query(query)

    def _insert_mensagem_anexos(self, itens: str):
        query = f"""
                INSERT INTO dbo.mensagem_anexos
                VALUES {itens}"""
        return self._exec_insert_query(query)


if __name__ == '__main__':
    teste_connection = MailAuditDAO()
