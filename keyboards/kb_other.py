from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_id = KeyboardButton("🆔айди")
button_support = KeyboardButton("📅Расписание")
button_info = KeyboardButton("🆘инфо")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_id,
    button_support,
    button_info,
)
