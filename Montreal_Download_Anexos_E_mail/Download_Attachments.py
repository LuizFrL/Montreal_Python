import imaplib, email, time, datetime, email.utils
import os
from Montreal_Download_Anexos_E_mail import Inf


def convert_data(string_email_data):
    date = email.utils.parsedate(string_email_data)
    date_email = datetime.datetime.fromtimestamp(time.mktime(date))
    return date_email.date()


u = Inf.user()
p = Inf.password()

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(u, p)

res = mail.select('Faturas')
result, data = mail.uid('search', None, 'ALL')

emails_inbox = data[0].split()

for uid_emails in emails_inbox:
    result2, email_data = mail.uid('fetch', uid_emails, '(RFC822)')
    raw = email.message_from_bytes(email_data[0][1])
    if convert_data(raw['Date']) == datetime.datetime.now().date():
        for part in raw.walk():
            if part.get_filename():
                if part.get_filename().find('.pdf') != -1:
                    print('Download:', part.get_filename(), '\nFrom:', raw['Subject'])
                    print()
                    with open(os.path.join(r'U:\Emails', part.get_filename()), 'wb') as file:
                        file.write(part.get_payload(decode=True))
