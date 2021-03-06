import imaplib, email, time, datetime, email.utils
import os
from email.header import decode_header, Header
import Inf


def convert_data(string_email_data, full=False):

    date = email.utils.parsedate(string_email_data)
    date_email = datetime.datetime.fromtimestamp(time.mktime(date))
    return date_email if full else date_email.date()


def mount_dir(date, filename):
    date = str(date)
    dir_e_mails = r'U:\E-mails'
    if os.path.exists(os.path.join(dir_e_mails, date)):
        return os.path.join(dir_e_mails, date, filename)

    os.mkdir(os.path.join(dir_e_mails, date))
    return os.path.join(dir_e_mails, date, filename)


def mount_attachment_name(attachment_name, subject):
    not_chars = ["\\", '/', '|', '*', '"', '?', '<', '>', '=', ':', '\n', '\r', '\t']
    correct_subject = "".join([char if char not in not_chars else "" for char in subject])
    attachment_name_correct = "".join([char if char not in not_chars else " " for char in attachment_name])
    return correct_subject + " & " + attachment_name_correct


if __name__ == '__main__':
    print('Versão 1.0.1')
    u = Inf.user()
    p = Inf.password()

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(u, p)

    move_folder = 'Teste'
    res = mail.select('inbox')
    result, data = mail.uid('search', None, f'(SENTSINCE {datetime.datetime.now().strftime("%d-%b-%Y")})')
    # '(UNSEEN)' para selecionar apenas emails não lidos,
    # f'(SENTSINCE {datetime.datetime.now().strftime("%d-%b-%Y")})' para e-mails de hoje
    # 'ALL' para procurar todos os e-mails
    emails_inbox = data[0].split()

    for uid_emails in emails_inbox:
        result2, email_data = mail.uid('fetch', uid_emails, '(RFC822)')
        raw = email.message_from_bytes(email_data[0][1])
        date_e_mail = convert_data(raw['Date'])
        subject = raw['Subject']
        header = decode_header(subject)[0]
        subject = str(Header(header[0], header[1] if not None else 'utf-8'))
        if date_e_mail == datetime.datetime.now().date():
            for part in raw.walk():
                attachment_name = part.get_filename()
                if attachment_name and os.path.splitext(attachment_name)[1].lower() in ('.pdf', '.PDF'):
                    attachment_name = mount_attachment_name(attachment_name, subject)
                    dire = mount_dir(date_e_mail, attachment_name)
                    with open(dire, 'wb') as file:
                        file.write(part.get_payload(decode=True))
                        print('Download feito com sucesso em,', dire)
                        print(f'Movendo e-mail "{subject}" para {move_folder}')
                        result = mail.uid('COPY', uid_emails, move_folder)
                        if result[0] == 'OK':
                            mov, data = mail.uid('STORE', uid_emails, '+FLAGS', '(\\Deleted)')
                            mail.expunge()
            print()
