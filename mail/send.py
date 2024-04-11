import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(receiver, theme, text, encode='utf-8'):
    """
    Отправка электронного письма (email)
    """

    mail_login = os.getenv("mail_login")
    password = os.getenv("mail_password")
    server = os.getenv("smtp_server")
    port = int(os.getenv("smtp_port"))
    charset = f'Content-Type: text/plain; charset={encode}'
    mime = 'MIME-Version: 1.0'

    # формируем тело письма
    body = "\r\n".join((f"From: {mail_login}", f"To: {receiver}",
                        f"Subject: {theme}", mime, charset, "", text))

    try:
        # подключаемся к почтовому сервису
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(mail_login, password)
        # пробуем послать письмо
        smtp.sendmail(mail_login, receiver, body.encode(encode))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()


