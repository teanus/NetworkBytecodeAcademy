from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from provider.database import db

button_id = KeyboardButton("🆔айди")
button_schedule = KeyboardButton("📅Расписание")
button_info = KeyboardButton("🆘инфо")
button_admin_panel = KeyboardButton("⚙Обновить данные")
button_communication = KeyboardButton("📧Связаться")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_id, button_schedule, button_info, button_admin_panel, button_communication
)

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

    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard
