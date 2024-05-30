from aiogram.utils import executor

from create_bot import dp
from handlers import admin, common, other


async def on_startup(_) -> None:
    """
    Функция, выполняющаяся при запуске бота.

    Выводит сообщение в консоль, что бот начал работу.
    """
    print("Бот начал работу!")


async def on_shutdown(_) -> None:
    """
    Функция, выполняющаяся при завершении работы бота.

    Выводит сообщение в консоль, что бот выключен.
    """
    print("Бот выключен")


# Регистрация обработчиков команд из разных модулей
admin.register_handlers_admin(dp)
common.register_handlers_common(dp)
other.register_handlers_other(dp)

if __name__ == "__main__":
    # Запуск long-polling
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
