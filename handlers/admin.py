from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiohttp import ClientError

from create_bot import bot
from keyboards import kb_admin
from provider import db


class AdminState(StatesGroup):
    """
    Класс для хранения состояний администратора.
    """

    set_settings = State()


async def settings(message: types.Message) -> None:
    """
    Обработчик команды для настройки расписания.

    Запрашивает у пользователя отправить документ в формате Excel (xlsx)
    для добавления расписания.

    Args:
        message (types.Message): Сообщение от пользователя.
    """
    await message.answer(
        "Пришли документ в формате excel (xlsx), для добавления расписания",
        reply_markup=kb_admin.back_menu,
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
                "Файл успешно обработан и расписание добавлено в базу данных!",
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


def register_handlers_admin(dp: Dispatcher) -> None:
    """
    Регистрирует обработчики команд для администраторов.

    Args:
        dp (Dispatcher): Диспетчер aiogram для регистрации обработчиков.
    """
    dp.register_message_handler(
        settings,
        Text(["⚙управление", "управление", "⚙settings", "settings"], ignore_case=True),
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
