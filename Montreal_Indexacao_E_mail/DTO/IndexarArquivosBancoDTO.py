from Montreal_Indexacao_E_mail.DAO.MailAudit.MailAuditDAO import MailAuditDAO
from Montreal_Indexacao_E_mail.Service.LerArquivoEmail import LerArquivoEmail
from Montreal_Download_Anexos_E_mail.Download_Attachments import convert_data


class IndexarAqruivosBancoDTO(MailAuditDAO):

    def __init__(self, arquivo_email: LerArquivoEmail):
        MailAuditDAO.__init__(self)
        self.arquivo_email = arquivo_email

    def inserir_dados_mensagens(self):
        dados = {
            'id_mensagem': self.arquivo_email.id_mensagem,
            'nome_do_arquivo': self.arquivo_email.get_dir_arquivo(),
            'message_id': self.arquivo_email.get_email_message_id(),
            'id_from': self.arquivo_email.emails_to[0]['id'],
            'header_subject': self.arquivo_email.get_email_subject(),
            'header_date': str(convert_data(self.arquivo_email.get_email_date(), full=True)),
            'body_text': self.arquivo_email.get_email_text()[0:127],
            'body_html': self.arquivo_email.get_email_html()[0:127]
    }
        return self._insert_mensagens(str(tuple(dados.values())))

    def inserir_dados_anexos(self):
        dados_anexo = self.arquivo_email.email_attachment_info
        query = ''
        if not dados_anexo:
            print('Sem anexo')
            return
        for index, anexo in enumerate(dados_anexo):
            query += f"""
('{anexo["id"]}', '{anexo["md5"]}', '{anexo["Name"]}', '{anexo["Content_Type"]}', '{anexo["Size"]}')"""
            if index + 1 != len(dados_anexo):
                query += ', '
        return self._insert_anexos(query)

    def inserir_dados_mensagem_to(self):
        query = ''
        for index, email in enumerate(self.arquivo_email.emails_to):
            query += f"('{self.arquivo_email.id_mensagem}', '{email['id']}')"
            if index + 1 != len(self.arquivo_email.emails_to):
                query += ', '

        return self._insert_mensagem_to(query)

    def inserir_dados_mensagem_anexos(self):
        todos_anexos = self.arquivo_email.email_attachment_info
        query = ''
        if not todos_anexos:
            print('Sem dados de anexo')
            return
        for index, anexo in enumerate(todos_anexos):
            query += f"""
        ('{self.arquivo_email.id_mensagem}', '{anexo["id"]}')"""
            if index + 1 != len(todos_anexos):
                query += ', '
        return self._insert_mensagem_anexos(query)

    def inserir_dados_endereco_emails(self):
        query = ''
        emails_to = self.arquivo_email.emails_to
        for index, emai in enumerate(emails_to):
            query += f"""( '{emai["id"]}', '{emai["Name"]}', '{emai["email"]}' )"""
            if index + 1 != len(emails_to):
                query += ', '
        self._insert_endereco_emails(query)


if __name__ == '__main__':
    pass
