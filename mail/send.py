import asyncio
import os

from aiosmtplib import SMTP, SMTPException
from dotenv import load_dotenv

load_dotenv()


async def send_email(receiver, theme, text, encode="utf-8"):
    """
    Асинхронная отправка электронного письма (email)
    """

    mail_login = os.getenv("mail_login")
    password = os.getenv("mail_password")
    server = os.getenv("smtp_server")
    port = int(os.getenv("smtp_port"))
    charset = f"Content-Type: text/plain; charset={encode}"
    mime = "MIME-Version: 1.0"

    # формируем тело письма
    body = "\r\n".join(
        (
            f"From: {mail_login}",
            f"To: {receiver}",
            f"Subject: {theme}",
            mime,
            charset,
            "",
            text,
        )
    )

    try:
        # подключаемся к почтовому сервису
        smtp = SMTP(hostname=server, port=port)
        await smtp.connect()
        await smtp.login(mail_login, password)
        # пробуем послать письмо
        await smtp.sendmail(mail_login, receiver, body.encode(encode))
    except SMTPException as err:
        print("Что-то пошло не так...")
        raise err
    finally:
        await smtp.quit()
