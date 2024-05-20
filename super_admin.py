#
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#
#
#
# ████████╗███████╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║██╔════╝
#    ██║   █████╗  ███████║██╔██╗ ██║██║   ██║███████╗
#    ██║   ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║╚════██║
#    ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝███████║
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

from resources import config

# Список ID администраторов
admins = [787110242]


async def get_state() -> bool:
    """
    Получает текущее состояние функции добавления супер-администратора из конфигурации.

    Returns:
        bool: True, если функция включена, иначе False.
    """
    return config.super_admin_add()["function"] == "on"


async def add_admin(user_id: int) -> None:
    """
    Добавляет пользователя в список администраторов.

    Args:
        user_id (int): Идентификатор пользователя, который нужно добавить в администраторы.
    """
    admins.append(user_id)


async def get_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.

    Args:
        user_id (int): Идентификатор пользователя для проверки.

    Returns:
        bool: True, если пользователь является администратором, иначе False.
    """
    return user_id in admins
