from Montreal_Indexacao_E_mail.DAO.MailAudit.MailAuditDAO import MailAuditDAO
from Montreal_Indexacao_E_mail.Service.LerArquivoEmail import LerArquivoEmail
from Montreal_Download_Anexos_E_mail.Download_Attachments import convert_data


class IndexarAqruivosBancoDTO(MailAuditDAO):

    def __init__(self, arquivo_email: LerArquivoEmail):
        MailAuditDAO.__init__(self)
        self.arquivo_email = arquivo_email

    def inserir_dados_dbo_mensagens(self):
        dados = {
            'id_mensagem': self.create_id_mensagem(),
            'nome_do_arquivo': self.arquivo_email.get_dir_arquivo(),
            'message_id': self.arquivo_email.get_email_message_id(),
            'id_from': self.create_id_from(),
            'header_subject': self.arquivo_email.get_email_subject(),
            'header_date': str(convert_data(self.arquivo_email.get_email_date(), full=True)),
            'body_text': self.arquivo_email.get_email_text(),
            'body_html': self.arquivo_email.get_email_html()
        }
        print(tuple(dados.values()))
        return self.insert_mensagens(tuple(dados.keys()))

    def create_id_email(self) -> str:
        pass

    def create_id_anexo(self) -> str:
        pass

    def create_id_mensagem(self) -> str:
        pass

    def create_id_from(self) -> str:
        pass


if __name__ == '__main__':
    b = LerArquivoEmail(r'C:\Users\m1015\Documents\E-mail\chamado - 17181\1580351016.Vca01I1a1ff0M735250.webmail.eml')
    a = IndexarAqruivosBancoDTO(b)
    a.inserir_dados_dbo_mensagens()
