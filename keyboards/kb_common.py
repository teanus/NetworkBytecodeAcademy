from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

back_button = KeyboardButton("◀отмена")
back_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)
