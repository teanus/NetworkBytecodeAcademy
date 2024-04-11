from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


async def id_cmd(message: types.Message) -> None:
    chat_id = message.chat.id
    await message.reply(f"Ваш id: {chat_id}")


async def info_cmd(message: types.Message) -> None:
    await message.reply(
        "Бот-помощник для колледжей"
    )


def register_handlers_other(dp: Dispatcher) -> None:
    dp.register_message_handler(
        id_cmd, Text(startswith=["🆔айди", "/id"], ignore_case=True)
    )
    dp.register_message_handler(
        info_cmd, Text(startswith=["🆘инфо", "/info"], ignore_case=True)
    )

