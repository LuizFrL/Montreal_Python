import email, os, uuid
import glob
import hashlib
from email.header import decode_header, Header


class LerArquivoEmail(object):

    def __init__(self, arquivo, dir_arquivo):
        self.dir_arquivo = dir_arquivo
        self.id_email = self.__create_id_email().upper()
        self.id_mensagem = self.__create_id_mensagem().upper()
        self.id_from = self.id_email
        self.msg = email.message_from_string(arquivo)
        self.emails_to = self._get_email_to()
        self.email_attachment_info = self._get_email_attachment_info()

    # @staticmethod
    # def get_msg_email(dir_arquivo):
    #     with open(dir_arquivo, 'r', encoding='utf-8') as f_email:
    #         return email.message_from_file(f_email)

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

    def __formatar_email_name(self, email: str):
        inf = {}
        if email.find("<") != -1:
            if email.find("<") != -1:
                name_email = email.replace('>', '').replace('"', '').replace('\n', "").replace("'", "")\
                    .replace('\t', "").split('<')
                inf['Name'], inf['email'] = self.__format_mime(name_email[0].strip()), name_email[1].strip()
        else:
            inf['Name'], inf["email"] = "", email
        inf['id'] = self.__create_id_email()
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

    def _get_email_to(self):
        return self.__formatar_email_cc_to()

    def get_email_date(self):
        return self.msg['Date']

    def get_email_subject(self):
        return self.__format_mime(self.msg['Subject'])

    def get_email_message_id(self):
        return self.msg['Message-ID']

    def get_email_text(self):
        texto = ''
        for part in self.msg.walk():
            if part.get_content_type() == 'text/plain':
                texto += part.get_payload()

        return self.__format_mime(texto)

    def get_email_html(self):
        return str(self.msg.get_payload()[0]).replace("'", "")

    def get_dir_arquivo(self):
        return self.dir_arquivo

    def _get_email_attachment_info(self):
        """
        Iformacoes dos arquivos de anexo no email,
        pra cada mensa
        """
        inf_attachments = []
        for pa in self.msg.walk():
            if pa.get_filename():
                attachment_content_type = {
                    'id': self.__create_id_anexo(pa.get_payload()),
                    'Name': self.__format_mime(pa.get_filename()),
                    'Content_Type': pa.get_content_type(),
                    'Size': self.__get_size_attachment(self.__format_mime(pa.get_filename()), pa.get_payload()),
                    'md5': hashlib.md5(pa.get_payload().encode()).hexdigest()
                }
                inf_attachments.append(attachment_content_type)
        return inf_attachments

    def __create_id_email(self) -> str:
        # """ ID gerado com a juncao do hash md5 do texto escrito no email (campo com as informacoes retornadas da
        # funcao get_email_text()) e com o hash md5 do seu payload (campo com as informacoes contidas na funcao
        # get_email_html()) """ return self.gerar_hash_md5(self.get_email_text()) + self.gerar_hash_md5(
        # self.get_email_html())
        return str(uuid.uuid4()).upper()

    def __create_id_anexo(self, payload) -> str:
        # """
        # ID gerado com a junção do hash md5 do id_email (retornado da funcao create_id_email()) com o hash md5
        # das informacoes dentro do anexo (payload do anexo).
        # """
        # return self.gerar_hash_md5(self.create_id_email()) + self.gerar_hash_md5(payload)
        return str(uuid.uuid4()).upper()

    def __create_id_mensagem(self) -> str:
        # """
        # ID gerado com a juncao do Id_email (funcao create_id_email()) com o hash md5 com as informacoes da
        # funcao get_email_message_id()
        # """
        # return self.create_id_email() + self.gerar_hash_md5(self.get_email_message_id())
        return str(uuid.uuid4()).upper()

    @staticmethod
    def __format_mime(text):
        header = decode_header(text)[0]
        return str(Header(header[0], header[1] if not None else 'utf-8'))


if __name__ == '__main__':
    b = LerArquivoEmail(r'C:\Users\m1015\Documents\E-mail\Faturas para pagamento - 28379 - 28387.eml', 'asdsad')
    print(b.msg)
