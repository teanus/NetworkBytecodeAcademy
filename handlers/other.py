from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from admin_code import ADMIN_CODE
from keyboards import get_main_menu
from super_admin import add_admin, get_admin, get_state


async def start(message: types.Message) -> None:
    """
    Обработчик команды /start.

    Проверяет, является ли пользователь администратором. Если да,
    отправляет сообщение с кнопками для управления расписанием.
    Если нет, отправляет приветственное сообщение с предложением зарегистрироваться.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    is_admin = await get_admin(message.from_user.id)
    menu = await get_main_menu(message.from_user.id)
    text = (
        'Ты администратор! Нажми на кнопку "управление" и измени расписание'
        if is_admin
        else "Привет друг! Введи /info для отображения информации о боте или зарегистрируйся"
    )
    await message.answer(text, reply_markup=menu)


async def code_admin(message: types.Message) -> None:
    """
    Обработчик для кода администратора.

    Проверяет состояние и, если все условия выполнены, назначает пользователя администратором.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    if await get_state():
        await add_admin(message.from_user.id)
        await message.reply("Вы теперь администратор! Поздравляю")


async def id_cmd(message: types.Message) -> None:
    """
    Обработчик команды для получения ID чата.

    Отправляет ID текущего чата пользователю.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    chat_id = message.chat.id
    await message.reply(f"Ваш id: {chat_id}")


async def info_cmd(message: types.Message) -> None:
    """
    Обработчик команды /info.

    Отправляет информацию о боте пользователю.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.reply("Бот-помощник для Network&Bytecode academy. ")


def register_handlers_other(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков команд.

    Регистрирует обработчики для команд администратора и общих команд.

    Args:
        dp (Dispatcher): Диспетчер aiogram для регистрации обработчиков.
    """
    dp.register_message_handler(code_admin, Text(equals=ADMIN_CODE))
    dp.register_message_handler(
        id_cmd, Text(startswith=["🆔айди", "/id"], ignore_case=True)
    )
    dp.register_message_handler(
        info_cmd, Text(startswith=["🆘инфо", "/info"], ignore_case=True)
    )
    dp.register_message_handler(start)
