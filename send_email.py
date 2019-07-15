from email.mime.text import MIMEText
import smtplib
from imaplib import IMAP4


def send_email(email,height):
    from_email="testemail.python@yandex.com"
    from_password="testPython"
    to_email=email

    subject="Height Data"

    message="Hey there, your height is <strong>%s</strong>." % height

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    yandex=smtplib.SMTP('smtp.yandex.com',465)
    # yandex=imaplib.IMAP4("imap.yandex.com",993)
    # yandex=smtplib.SMTP('smtp.gmail.com',)
    yandex.ehlo()
    yandex.starttls()
    yandex.login(from_email,from_password)
    yandex.send_message(msg)
