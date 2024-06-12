from aiogram import types

import super_admin
from keyboards import kb_admin, kb_other


async def get_main_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    """
    Возвращает главное меню на основе идентификатора пользователя.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        types.ReplyKeyboardMarkup: Главное меню для пользователя.
    """

    return kb_admin.main_menu if user_id in super_admin.admins else kb_other.main_menu
