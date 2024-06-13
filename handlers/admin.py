from functools import wraps
from typing import Any, Callable

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiohttp import ClientError

from super_admin import admin
from create_bot import bot
from keyboards import kb_admin, kb_common
from mail import send_email
from provider import db


class AdminState(StatesGroup):
    """
    Класс для хранения состояний администратора.
    """

    set_settings = State()
    get_group_name_to_email = State()
    get_message_to_email = State()


def admin_required(
    handler: Callable[[types.Message, Any], Any]
) -> Callable[[types.Message, Any], Any]:
    """
    Декоратор для проверки прав администратора.

    Этот декоратор проверяет, является ли пользователь администратором,
    перед выполнением обработчика. Если пользователь не администратор,
    возвращается сообщение о недостатке прав.

    Args:
        handler (Callable[[types.Message, Any], Any]): Функция-обработчик, которая будет выполняться,
                                                       если пользователь администратор.

    Returns:
        Callable[[types.Message, Any], Any]: Обёрнутая функция-обработчик.
    """

    @wraps(handler)
    async def wrapper(message: types.Message, *args: Any, **kwargs: Any) -> Any:
        if await admin.get_admin(message.from_user.id):
            return await handler(message, *args, **kwargs)
        else:
            await message.reply("У вас нет прав для выполнения этой команды.")

    return wrapper


@admin_required
async def settings(message: types.Message) -> None:
    """
    Обработчик команды для настройки расписания.

    Запрашивает у пользователя отправить документ в формате Excel (xlsx)
    для добавления расписания.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.answer(
        "Пришли документ в формате excel (xlsx), для добавления данных",
        reply_markup=kb_common.back_menu,
    )
    await AdminState.set_settings.set()


async def cancel_settings(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды для отмены настройки расписания.

    Завершает состояние настройки и возвращает пользователя в главное меню.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    await message.reply("Вы вышли из админ панели", reply_markup=kb_admin.main_menu)
    await state.finish()


async def get_document(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды для получения и обработки документа.

    Проверяет, что документ является файлом Excel, загружает его, читает содержимое,
    вставляет данные в базу данных и завершает состояние настройки.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    try:
        if (
            message.document.mime_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            file_id = message.document.file_id
            file_info = await bot.get_file(file_id)
            downloaded_file = await bot.download_file(file_info.file_path)

            excel_bytes = downloaded_file.read()
            await db.insert_data_from_excel(excel_bytes)
            await message.reply(
                "Файл успешно обработан и данные добавлены в базу данных!",
                reply_markup=kb_admin.main_menu,
            )
            await state.finish()
        else:
            await message.reply("Пожалуйста, пришлите файл в формате Excel.")
    except ClientError as e:
        await message.reply(
            f"Произошла ошибка при загрузке файла: {str(e)}. Пожалуйста, попробуйте еще раз."
        )
    except Exception as e:
        await message.reply(
            f"Произошла неизвестная ошибка: {str(e)}. Пожалуйста, попробуйте еще раз или обратитесь к "
            f"администратору."
        )


@admin_required
async def set_group_name(message: types.Message) -> None:
    """
    Обработчик команды для выбора группы.

    Отправляет сообщение с кнопками для выбора группы.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    group_buttons = await kb_common.create_group_inline_buttons()
    await message.answer(
        "Ты вошел в систему отправки сообщений на почту",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await message.answer("Выбери группу:", reply_markup=group_buttons)
    await AdminState.get_group_name_to_email.set()


async def back_to_main_menu(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.answer(
        "Возвращение в главное меню.", reply_markup=kb_admin.main_menu
    )
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.answer()
    await state.finish()


async def group_name_callback_handler(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """
    Обработчик выбора группы из инлайн-кнопок.

    Сохраняет выбранное название группы в состояние и запрашивает текст сообщения.

    Args:
        callback_query (CallbackQuery): Объект колбека от инлайн-кнопки.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    group_name = callback_query.data
    async with state.proxy() as data:
        data["group_name"] = group_name
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(
        "Пришли текст сообщения",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="Назад")]], resize_keyboard=True
        ),
    )
    await AdminState.get_message_to_email.set()
    await callback_query.answer()


async def get_text_message_to_email(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик получения текста сообщения для отправки на email.

    Получает текст сообщения, отправляет его на email адреса группы и завершает состояние.

    Args:
        message (types.Message): Сообщение от пользователя.
        state (FSMContext): Состояние Finite State Machine (FSM) контекста.
    """
    async with state.proxy() as data:
        group_name = data.get("group_name")
    if message.text.lower() == "назад":
        await back_to_group_selection(message)
    elif group_name:
        emails = await db.get_emails_by_group(group_name)
        if emails:
            await message.answer(
                "Сообщения отправлены!", reply_markup=types.ReplyKeyboardRemove()
            )
            await send_email(receivers=emails, text=message.text)
        else:
            await message.answer(
                "Не найдены адреса электронной почты для указанной группы.",
                reply_markup=types.ReplyKeyboardRemove(),
            )
    else:
        await message.answer(
            "Не удалось получить название группы. Пожалуйста, отправьте название группы заново.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    await state.finish()


async def back_to_group_selection(message: types.Message) -> None:
    group_buttons = await kb_common.create_group_inline_buttons()
    await message.answer("Вернулись назад!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Выбери группу:", reply_markup=group_buttons)
    await AdminState.get_group_name_to_email.set()


def register_handlers_admin(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд для администраторов.

    Args:
        dp (Dispatcher): Диспетчер aiogram для регистрации обработчиков.
    """
    dp.register_message_handler(
        settings,
        Text(
            ["⚙Обновить данные", "управление", "⚙settings", "settings"],
            ignore_case=True,
        ),
    )
    dp.register_message_handler(
        cancel_settings,
        Text(["◀отмена", "отмена", "cancel", "back"], ignore_case=True),
        state=AdminState.set_settings,
    )
    dp.register_message_handler(
        get_document,
        state=AdminState.set_settings,
        content_types=[types.ContentType.DOCUMENT],
    )
    dp.register_message_handler(
        set_group_name, Text(["📧Связаться", "📧Communication"], ignore_case=True)
    )

    dp.register_callback_query_handler(
        back_to_main_menu,
        lambda c: c.data == "назад",
        state=AdminState.get_group_name_to_email,
    )

    dp.register_callback_query_handler(
        group_name_callback_handler, state=AdminState.get_group_name_to_email
    )

    dp.register_message_handler(
        back_to_group_selection,
        Text("Назад", ignore_case=True),
        state=AdminState.get_message_to_email,
    )

    dp.register_message_handler(
        get_text_message_to_email, state=AdminState.get_message_to_email
    )
