import secrets
import time

from mail import send_email
from provider import db


async def generate_code(email):
    # Генерация случайного кода
    code = secrets.token_hex(3)

    # Сохранение кода в базе данных
    await db.save_code(email, code=code)

    await send_email(email, "Регистрация", f"Ваш код для регистрации: {code}")

    return code


async def verify_code(email, code):
    rows = await db.get_code(email)  # Получаем все коды для указанной почты
    # Проверка каждого кода
    for saved_code, timestamp in rows:
        # Проверка соответствия кода
        if saved_code == code:
            # Проверка времени создания кода
            if time.time() - timestamp <= 180:
                return True
    return False
