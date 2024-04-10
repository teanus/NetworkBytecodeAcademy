from aiogram.utils import executor


from create_bot import dp
from handlers import admin, student, other


async def on_startup(_) -> None:
    print("Бот начал работу!")


async def on_shutdown(_) -> None:
    print("Бот выключен")


admin.register_handlers_admin(dp)
student.register_handlers_client(dp)
other.register_handlers_other(dp)


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )