from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_id = KeyboardButton("🆔айди")
button_schedule = KeyboardButton("📅Расписание")
button_info = KeyboardButton("🆘инфо")
button_admin_panel = KeyboardButton("⚙Обновить данные")
button_communication = KeyboardButton("📧Связаться")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    button_id, button_schedule, button_info, button_admin_panel, button_communication
)
