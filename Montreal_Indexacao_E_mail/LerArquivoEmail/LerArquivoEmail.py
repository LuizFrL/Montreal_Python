import email


class LerArquivoEmail(object):

    def __init__(self, arquivo):
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
        return self.msg.get_payload()[0]

    def get_dir_arquivo(self):
        return self.dir_arquivo
