from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery

from keyboards import get_main_menu, kb_common
from provider import db


class CommonState(StatesGroup):
    """
    Класс для хранения состояний пользователя.
    """

    get_group_schedule = State()


# 1
async def get_group(message: types.Message) -> None:
    """
    Обработчик команды для запроса группы.

    Отправляет инлайн-клавиатуру с кнопками для выбора группы.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    group_buttons = await kb_common.create_group_inline_buttons()

    await message.answer(
        "Выберите группу, расписание которой хотите узнать:", reply_markup=group_buttons
    )
    await CommonState.get_group_schedule.set()


async def group_schedule_callback_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """
    Обработчик выбора группы из инлайн-кнопок для получения расписания.

    Получает расписание группы из базы данных и отправляет его пользователю.

    Args:
        callback_query (CallbackQuery): Объект колбека от инлайн-кнопки.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    if await state.get_state() != CommonState.get_group_schedule.state:
        await callback_query.answer("Действие отменено.")
        return

    group_name = callback_query.data

    # Если нажата кнопка "Отмена", то завершаем состояние и возвращаем пользователя в главное меню
    if group_name == "назад":
        await state.finish()
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.message.answer(
            "Возвращаемся в меню",
            reply_markup=await get_main_menu(callback_query.from_user.id),
        )
        await callback_query.answer()
        return

    # Удаляем инлайн-клавиатуру
    await callback_query.message.edit_reply_markup(reply_markup=None)

    # Получаем расписание и отправляем его
    schedule = await db.get_weekly_schedule_by_group(group_name.lower())
    await callback_query.message.answer(schedule, parse_mode="Markdown")
    await state.finish()
    await callback_query.answer()


def register_handlers_common(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд для общих запросов.

    Args:
        dp (Dispatcher): Диспетчер aiogram для регистрации обработчиков.
    """

    dp.register_message_handler(
        get_group, Text(["📅Расписание", "Расписание", "schedule"], ignore_case=True)
    )
    dp.register_callback_query_handler(
        group_schedule_callback_handler, state=CommonState.get_group_schedule
    )
