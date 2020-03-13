import email, os, uuid
import glob
import hashlib


class LerArquivoEmail(object):

    def __init__(self, arquivo):
        self.dir_arquivo = arquivo
        self.id_email = self.__create_id_email().upper()
        self.id_mensagem = self.__create_id_mensagem().upper()
        self.id_from = self.id_email
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

    @staticmethod
    def __formatar_email_name(email: str):
        inf = {}
        if email.find("<") != -1:
            if email.find("<") != -1:
                name_email = email.replace('>', '').replace('"', '').replace('\n', "").replace('\t', "").split('<')
                inf['Name'], inf['email'] = name_email[0].strip(), name_email[1].strip()
        else:
            inf['Name'], inf["email"] = "", email
        return inf

    def __formatar_email_cc_to(self):
        names_emails = []
        for form in ['To', 'CC']:
            if self.msg[form]:
                if self.msg[form].find(',') != -1:
                    emails_to = self.msg[form].split(',')
                    for em_to in emails_to:
                        em_to_clean = em_to.strip().replace('	', '').replace('\n', '')
                        names_emails.append(self.__formatar_email_name(em_to_clean))
                else:
                    names_emails.append(self.__formatar_email_name(self.msg[form]))
        return names_emails

    def get_email_from(self):
        return self.msg['From']

    def get_email_to(self):
        return self.__formatar_email_cc_to()

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
        """
        Iformacoes dos arquivos de anexo no email,
        pra cada mensa
        """
        inf_attachments = []
        for pa in self.msg.walk():
            if pa.get_filename():
                attachment_content_type = {
                    'id': self.__create_id_anexo(pa.get_payload()),
                    'Name': pa.get_filename(),
                    'Content_Type': pa.get_content_type(),
                    'Size': self.__get_size_attachment(pa.get_filename(), pa.get_payload()),
                    'md5': hashlib.md5(pa.get_payload().encode()).hexdigest()
                }
                inf_attachments.append(attachment_content_type)
        return inf_attachments

    def __create_id_email(self) -> str:
        # """ ID gerado com a juncao do hash md5 do texto escrito no email (campo com as informacoes retornadas da
        # funcao get_email_text()) e com o hash md5 do seu payload (campo com as informacoes contidas na funcao
        # get_email_html()) """ return self.gerar_hash_md5(self.get_email_text()) + self.gerar_hash_md5(
        # self.get_email_html())
        return str(uuid.uuid4())

    def __create_id_anexo(self, payload) -> str:
        # """
        # ID gerado com a junção do hash md5 do id_email (retornado da funcao create_id_email()) com o hash md5
        # das informacoes dentro do anexo (payload do anexo).
        # """
        # return self.gerar_hash_md5(self.create_id_email()) + self.gerar_hash_md5(payload)
        return str(uuid.uuid4())

    def __create_id_mensagem(self) -> str:
        # """
        # ID gerado com a juncao do Id_email (funcao create_id_email()) com o hash md5 com as informacoes da
        # funcao get_email_message_id()
        # """
        # return self.create_id_email() + self.gerar_hash_md5(self.get_email_message_id())
        return str(uuid.uuid4())


if __name__ == '__main__':
    a = glob.glob(r'C:\Users\m1015\Documents\E-mail\**\**', recursive=True)
    # print(a)
    # exit()
    # for di in glob.glob(r'C:\Users\m1015\Documents\E-mail\**\**', recursive=True):
    di = r'C:\Users\m1015\Documents\1575226347.Vca01I1c2406M664469.webmail%3A2,'
    e_m = LerArquivoEmail(di)
    print(e_m.get_email_to())
    print()
