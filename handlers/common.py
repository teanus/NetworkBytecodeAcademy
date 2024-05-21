from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards import kb_common, get_main_menu
from provider import db


class CommonState(StatesGroup):
    """
    Класс для хранения состояний пользователя.
    """

    get_group_schedule = State()


async def get_group(message: types.Message) -> None:
    """
    Обработчик команды для запроса группы.

    Запрашивает у пользователя ввести название группы, расписание которой он хочет узнать.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.answer(
        "Введите группу расписание которой хотите узнать",
        reply_markup=kb_common.back_menu,
    )
    await CommonState.get_group_schedule.set()


async def send_subject(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды для отправки расписания группы.

    Получает расписание группы из базы данных и отправляет его пользователю.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    await message.answer(
        await db.get_weekly_schedule_by_group(message.text.lower()),
        parse_mode="Markdown",
    )


async def cancel_to_group(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды для отмены запроса группы.

    Возвращает пользователя назад в главное меню и завершает состояние запроса группы.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    await message.answer(
        "Возвращаемся назад!", reply_markup=await get_main_menu(message.from_user.id)
    )
    await state.finish()


def register_handlers_common(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд для общих запросов.

    Args:
        dp (Dispatcher): Диспетчер aiogram для регистрации обработчиков.
    """
    dp.register_message_handler(
        get_group, Text(["📅Расписание", "Расписание", "schedule"], ignore_case=True)
    )
    dp.register_message_handler(
        cancel_to_group,
        Text(["◀отмена", "отмена", "cancel", "back"], ignore_case=True),
        state=CommonState.get_group_schedule,
    )
    dp.register_message_handler(send_subject, state=CommonState.get_group_schedule)
