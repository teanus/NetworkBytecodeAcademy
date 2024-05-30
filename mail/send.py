import os
from aiosmtplib import SMTP, SMTPException
from dotenv import load_dotenv
from typing import List
from mail.validate import validate_email

load_dotenv()


async def send_email(receivers: List[str], theme: str = "Уведомление от NBA", text: str = "МЫУ",
                     encode: str = "utf-8") -> None:
    """
    Асинхронная отправка электронного письма (email).

    Args:
        receivers (List[str]): Список адресатов.
        theme (str): Тема письма. По умолчанию "Уведомление от NBA".
        text (str): Текст письма. По умолчанию "МЫУ".
        encode (str): Кодировка письма. По умолчанию "utf-8".

    Raises:
        SMTPException: Исключение, возникающее при ошибке отправки письма.
    """

    mail_login = os.getenv("mail_login")
    password = os.getenv("mail_password")
    server = os.getenv("smtp_server")
    port = int(os.getenv("smtp_port"))
    charset = f"Content-Type: text/plain; charset={encode}"
    mime = "MIME-Version: 1.0"

    # Формируем тело письма
    body = "\r\n".join(
        (
            f"From: {mail_login}",
            f"Subject: {theme}",
            mime,
            charset,
            "",
            text,
        )
    )
    smtp = None
    try:
        # Подключаемся к почтовому сервису
        smtp = SMTP(hostname=server, port=port)
        await smtp.connect()
        await smtp.login(mail_login, password)

        for receiver in receivers:
            if not await validate_email(receiver):
                continue
            else:
                # Формируем заголовок для каждого адресата
                receiver_header = f"To: {receiver}"
                full_body = "\r\n".join((receiver_header, body))

                # Пробуем послать письмо
                await smtp.sendmail(mail_login, receiver, full_body.encode(encode))
    except SMTPException as err:
        print("Что-то пошло не так...")
        raise err
    finally:
        await smtp.quit()
