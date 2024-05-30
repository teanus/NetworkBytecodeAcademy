import re


async def validate_email(email: str) -> bool:
    """
    Проверяет, является ли переданная строка допустимым email-адресом.

    Args:
        email (str): Строка, содержащая email-адрес для проверки.

    Returns:
        bool: True, если email-адрес допустим, False в противном случае.
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))
