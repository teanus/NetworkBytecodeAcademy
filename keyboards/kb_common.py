from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from provider import db

back_button = KeyboardButton("◀отмена")
back_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)


async def create_group_inline_buttons() -> InlineKeyboardMarkup:
    """
    Создает инлайн-кнопки для выбора групп.

    Возвращает:
        InlineKeyboardMarkup: Разметка с инлайн-кнопками для выбора групп.
    """
    groups = await db.get_all_groups()  # Получаем список групп

    keyboard = InlineKeyboardMarkup()
    for group in groups:
        keyboard.add(InlineKeyboardButton(text=group, callback_data=group))

    keyboard.add(InlineKeyboardButton(text="◀Отмена", callback_data="назад"))
    return keyboard
