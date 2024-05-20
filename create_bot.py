import os

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создание экземпляра MemoryStorage для хранения состояний FSM
storage = MemoryStorage()

# Инициализация бота с использованием токена из переменных окружения
bot = Bot(os.getenv("TOKEN"))

# Создание диспетчера для обработки сообщений и состояний
dp = Dispatcher(bot, storage=storage)
