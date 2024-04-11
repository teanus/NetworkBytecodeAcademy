import secrets
import time

from mail import send_email
from provider import db


class RegistrationManager:
    def __init__(self):
        self.db = db

    async def generate_code(self, email):
        # Генерация случайного кода
        code = secrets.token_hex(3)

        # Сохранение кода в базе данных
        await self.db.save_code(email, code=code)

        send_email(email, "Регистрация", f"Ваш код для регистрации: {code}")

        return code

    async def verify_code(self, email, code):
        # Проверка наличия кода для указанной почты в базе данных
        saved_code = await self.db.get_code(email)
        if saved_code == code:
            # Получение времени создания кода для указанной почты из базы данных
            timestamp = await self.db.get_code_timestamp(email)
            if timestamp:
                # Проверка времени жизни кода (3 минуты)
                if time.time() - timestamp <= 180:
                    return True
        return False


async def main():
    registration_manager = RegistrationManager()

    email = "teanus.ti@gmail.com"
    await registration_manager.generate_code(email)

    entered_code = input("Введите код из письма: ")
    if await registration_manager.verify_code(email, entered_code):
        print("Код верный. Регистрация прошла успешно.")
    else:
        print("Код неверный или устарел.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
