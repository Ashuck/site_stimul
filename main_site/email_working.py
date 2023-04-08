import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from stimul.settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_PASSWORD, DEFAULT_TO_EMAIL


def send_mail(text, subject):
    server = EMAIL_HOST
    sender = EMAIL_HOST_USER

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = DEFAULT_TO_EMAIL
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['Bcc'] = sender

    part_html = MIMEText(text, 'plain',  'utf-8')
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(EMAIL_HOST_USER, EMAIL_PASSWORD)
    mail.sendmail(sender, DEFAULT_TO_EMAIL, msg.as_string())
    mail.quit()

