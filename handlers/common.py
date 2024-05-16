from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_common
from provider import db


class CommonState(StatesGroup):
    hello_reg = State()  # состояние, где приветствуют при регистрации
    input_email = State()  # состояние, где вводят логин
    input_code = State()  # состояние, где вводят код


async def start(message: types.Message):
    await message.reply(
        "Привет друг! Введи /info для отображения информации о боте или зарегистрируйся",
        reply_markup=kb_common.main_menu,
    )


async def get_subject(message: types.Message):
    await message.reply(await db.get_weekly_schedule_by_group("PO214"))


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(get_subject, Text("расписание"))
    dp.register_message_handler(start)
