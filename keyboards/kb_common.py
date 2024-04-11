from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

listKb = ['кнопка 1', 'кнопка 2', 'кнопка 3']

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# Добавляем кнопки из списка в клавиатуру
for button_text in listKb:
    keyboard.add(KeyboardButton(button_text))

button_id = KeyboardButton("🆔айди")
button_info = KeyboardButton("🆘инфо")
button_support = KeyboardButton("🆘поддержка")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_id, button_info, button_support
)
