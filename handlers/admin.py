from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_admin


class AdminState(StatesGroup):
    pass


def register_handlers_admin(dp: Dispatcher) -> None:
    pass
