from aiogram import Dispatcher, types

from keyboards import kb_common


async def start(message: types.Message):
    chat_id = message.chat.id

    await message.reply(
        "Привет друг! Введи /info для отображения информации о боте!",
        reply_markup=kb_common.keyboard,
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start)
