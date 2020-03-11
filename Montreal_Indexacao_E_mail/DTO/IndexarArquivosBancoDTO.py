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
            'id_from': self.arquivo_email.id_from,
            'header_subject': self.arquivo_email.get_email_subject(),
            'header_date': str(convert_data(self.arquivo_email.get_email_date(), full=True)),
            'body_text': self.arquivo_email.get_email_text(),
            'body_html': self.arquivo_email.get_email_html()
        }
        #return self.insert_mensagens(tuple(dados.keys()))
        return dados

    def inserir_dados_anexos(self):
        dados_anexo = self.arquivo_email.get_email_attachment_info()
        inserir = ''
        for index, anexo in enumerate(dados_anexo):
            inserir += f"""
('{anexo["id"]}', '{anexo["md5"]}', '{anexo["Name"]}', '{anexo["Content_Type"]}', '{anexo["Size"]}')"""
            if index + 1 != len(dados_anexo):
                inserir += ', '
        #return self.insert_anexos(inserir)
        return inserir

    def inserir_dados_mensagem_to(self):
        pass

    def inserir_dados_mensagem_anexos(self):
        pass

    def inserir_dados_endereco_emails(self):
        pass


if __name__ == '__main__':
    b = LerArquivoEmail(r'C:\Users\m1015\Documents\E-mail\Faturas para pagamento - 28379 - 28387.eml')
    a = IndexarAqruivosBancoDTO(b)
    c = a.inserir_dados_anexos()
    print(c)
