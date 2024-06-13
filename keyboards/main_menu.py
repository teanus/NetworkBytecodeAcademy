from aiogram import types

from super_admin import admin
from keyboards import kb_admin, kb_other


async def get_main_menu(user_id: int) -> types.ReplyKeyboardMarkup:
    """
    Возвращает главное меню на основе идентификатора пользователя.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        types.ReplyKeyboardMarkup: Главное меню для пользователя.
    """

    return kb_admin.main_menu if admin.get_admin(user_id) else kb_other.main_menu
