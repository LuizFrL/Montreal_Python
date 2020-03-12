import email, os
import hashlib


class LerArquivoEmail(object):

    def __init__(self, arquivo):
        self.dir_arquivo = arquivo
        self.msg = self.get_msg_email(arquivo)

    @staticmethod
    def get_msg_email(dir_arquivo):
        with open(dir_arquivo, 'r', encoding='utf-8') as f_email:
            return email.message_from_file(f_email)

    @staticmethod
    def gerar_hash_md5(informacoes):
        return hashlib.md5(str(informacoes).encode()).hexdigest()

    @staticmethod
    def __get_size_attachment(name, payload):
        with open(name, 'w') as f:
            f.write(payload)
            size = os.stat(name).st_size
        os.unlink(name)
        return size

    def get_email_from(self):
        return self.msg['From']

    def get_email_to(self):
        if self.msg['To']:
            return self.msg['To']
        return self.msg['CC']

    def get_email_date(self):
        return self.msg['Date']

    def get_email_subject(self):
        return self.msg['Subject']

    def get_email_message_id(self):
        return self.msg['Message-ID']

    def get_email_text(self):
        texto = ''
        for part in self.msg.walk():
            if part.get_content_type() == 'text/plain':
                texto += part.get_payload()
        return texto

    def get_email_html(self):
        return str(self.msg.get_payload()[0])

    def get_dir_arquivo(self):
        return self.dir_arquivo

    def get_email_attachment_info(self):
        inf_attachments = []
        for pa in self.msg.walk():
            if pa.get_filename():
                attachment_content_type = {
                    'id': self.create_id_anexo(pa.get_payload()),
                    'Name': pa.get_filename(),
                    'Content_Type': pa.get_content_type(),
                    'Size': self.__get_size_attachment(pa.get_filename(), pa.get_payload()),
                    'md5': hashlib.md5(pa.get_payload().encode()).hexdigest()
                }
                inf_attachments.append(attachment_content_type)
        return inf_attachments

    def create_id_email(self):
        """
        ID gerado com a juncao do hash md5 do texto escrito no email (campo com as informacoes retornadas da funcao
        get_email_text()) e com o hash md5 do seu payload (campo com as informacoes contidas na funcao get_email_html())
        """
        return self.gerar_hash_md5(self.get_email_text()) + self.gerar_hash_md5(self.get_email_html())

    def create_id_anexo(self, payload) -> str:
        """
        ID gerado com a junção do hash md5 do id_email (retornado da funcao create_id_email()) com o hash md5
        das informacoes dentro do anexo (payload do anexo).
        """
        return self.gerar_hash_md5(self.create_id_email()) + self.gerar_hash_md5(payload)

    def create_id_mensagem(self) -> str:
        """
        ID gerado com a juncao do Id_email (funcao create_id_email()) com o hash md5 com as informacoes da
        funcao get_email_message_id()
        """
        return self.create_id_email() + self.gerar_hash_md5(self.get_email_message_id())

    def create_id_from(self) -> str:
        """
        ID gerado com a informacao gerada pelo hash md5 da funcao get_email_from()
        """
        return self.gerar_hash_md5(self.get_email_from())


if __name__ == '__main__':
    # for di in glob.glob(r'C:\Users\m1015\Documents\E-mail\**\*.eml', recursive=True):
    di = r'C:\Users\m1015\Documents\E-mail\Faturas para pagamento - 28379 - 28387.eml'
    e_m = LerArquivoEmail(di)
    print(e_m.get_email_attachment_info())
