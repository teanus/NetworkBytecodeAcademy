from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from auth.auth import generate_code, verify_code
from keyboards import kb_common
from mail import validate_email


class CommonState(StatesGroup):
    hello_reg = State()  # состояние, где приветствуют при регистрации
    input_email = State()  # состояние, где вводят логин
    input_code = State()  # состояние, где вводят код


async def start(message: types.Message):
    await message.reply(
        "Привет друг! Введи /info для отображения информации о боте или зарегистрируйся",
        reply_markup=kb_common.main_menu,
    )


async def hello_registration(message: types.Message):
    chat_id = message.chat.id
    await message.reply("Отправь свою почту для регистрации")
    await CommonState.input_email.set()


async def input_email_registration(message: types.Message, state: FSMContext):
    if not validate_email(message.text):
        await message.reply("Это не является почтой, повторите еще раз")
        return
    await state.update_data(email=message.text)
    await generate_code(message.text)
    await message.reply("Введите код")
    await CommonState.input_code.set()


async def input_code_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not await verify_code(email=data.get("email"), code=message.text):
        await message.reply("Это не верный код, введите еще раз")
        return
    await message.reply("Вы успешно зарегистрировались!")
    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(
        hello_registration, Text(startswith="🆘Регистрация", ignore_case=True)
    )
    dp.register_message_handler(input_email_registration, state=CommonState.input_email)
    dp.register_message_handler(input_code_registration, state=CommonState.input_code)
    dp.register_message_handler(start)
