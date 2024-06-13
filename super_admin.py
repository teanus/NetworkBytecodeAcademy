import json
from resources import config

ADMINS_FILE = 'admins.json'


class AdminManager:
    def __init__(self):
        self.admins = self.load_admins()

    @staticmethod
    def load_admins() -> list:
        try:
            with open(ADMINS_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_admins(self) -> None:
        with open(ADMINS_FILE, 'w') as file:
            json.dump(self.admins, file)

    @staticmethod
    async def get_state() -> bool:
        """
        Получает текущее состояние функции добавления супер-администратора из конфигурации.

        Returns:
            bool: True, если функция включена, иначе False.
        """
        return config.super_admin_add()["function"] == "on"

    async def add_admin(self, user_id: int) -> None:
        """
        Добавляет пользователя в список администраторов.

        Args:
            user_id (int): Идентификатор пользователя, который нужно добавить в администраторы.
        """
        if user_id not in self.admins:
            self.admins.append(user_id)
            self.save_admins()
            print(f"Добавлен новый администратор: {user_id}")
        else:
            print(f"Пользователь {user_id} уже является администратором")
        print(f"Текущий список администраторов: {self.admins}")

    async def get_admin(self, user_id: int) -> bool:
        """
        Проверяет, является ли пользователь администратором.

        Args:
            user_id (int): Идентификатор пользователя для проверки.

        Returns:
            bool: True, если пользователь является администратором, иначе False.
        """
        return user_id in self.admins


admin = AdminManager()
