from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_id = KeyboardButton("🆔айди")
button_schedule = KeyboardButton("📅Расписание")
button_info = KeyboardButton("🆘инфо")
button_admin_panel = KeyboardButton("⚙управление")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_id, button_schedule, button_info, button_admin_panel
)

back_button = KeyboardButton("◀отмена")
back_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)
