import email, glob, os


class LerArquivoEmail(object):

    def __init__(self, arquivo):
        self.id_from = self.create_id_from()
        self.id_mensagem = self.create_id_mensagem()
        self.dir_arquivo = arquivo
        self.msg = self.get_msg_email(arquivo)

    @staticmethod
    def get_msg_email(dir_arquivo):
        with open(dir_arquivo) as f_email:
            return email.message_from_file(f_email)

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

    def get_email_attachment_content_type(self):
        inf_attachments = []
        for pa in self.msg.walk():
            if pa.get_filename():
                attachment_content_type = {
                    'id': self.create_id_anexo(),
                    'Name': pa.get_filename(),
                    'Content_Type': pa.get_content_type(),
                    'Size': self.__get_size_attachment(pa.get_filename(), pa.get_payload())
                }
                inf_attachments.append(attachment_content_type)
        return inf_attachments

    def __get_size_attachment(self, name, payload):
        with open(name, 'w') as f:
            f.write(payload)
            size = os.stat(name).st_size
        os.unlink(name)
        return size

    def create_id_email(self):
        pass

    def create_id_anexo(self) -> str:
        pass

    def create_id_mensagem(self) -> str:
        pass

    def create_id_from(self) -> str:
        pass


if __name__ == '__main__':
    # for di in glob.glob(r'C:\Users\m1015\Documents\E-mail\**\*.eml', recursive=True):
    di = r'C:\Users\m1015\Documents\E-mail\Faturas para pagamento - 28379 - 28387.eml'
    e_m = LerArquivoEmail(di)
    print(e_m.get_email_attachment_content_type())
