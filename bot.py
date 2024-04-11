from aiogram.utils import executor

from create_bot import dp
from handlers import admin, common, other, student


async def on_startup(_) -> None:
    print("Бот начал работу!")


async def on_shutdown(_) -> None:
    print("Бот выключен")


admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
common.register_handlers_common(dp)

if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
