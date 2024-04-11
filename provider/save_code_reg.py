import time

import aiosqlite


class SqliteSaveCode:
    def __init__(self):
        self.connection = None
        self.cursor = None

    async def connect(self):
        try:
            self.connection = await aiosqlite.connect("save_code.db")
            self.cursor = await self.connection.cursor()
            if self.connection:
                print("SQLite подключился")
            table_save_code = (
                "CREATE TABLE IF NOT EXISTS registration_codes(id INTEGER PRIMARY KEY,email TEXT, "
                "code TEXT, timestamp REAL) "
            )

            await self.execute_query(table_save_code)

        except aiosqlite.Error as error:
            print(f"Ошибка при подключении к базе данных SQLite: {error}")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str, params=None):
        try:
            if not self.connection:
                await self.connect()
            if params:
                await self.cursor.execute(query, params)
            else:
                await self.cursor.execute(query)
            await self.connection.commit()
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")

    async def fetch_all(self, query: str, params=None):
        try:
            if not self.connection:
                await self.connect()
            if params:
                await self.cursor.execute(query, params)
            else:
                await self.cursor.execute(query)
            rows = await self.cursor.fetchall()
            return rows
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return []

    async def fetch_one(self, query: str, params=None):
        try:
            if not self.connection:
                await self.connect()
            if params:
                await self.cursor.execute(query, params)
            else:
                await self.cursor.execute(query)
            row = await self.cursor.fetchone()
            return row
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return None

    async def save_code(self, email, code):
        try:
            await self.execute_query(
                "INSERT OR REPLACE INTO registration_codes (email, code, timestamp) VALUES (?, ?, ?)",
                (email, code, time.time()),
            )
        except aiosqlite.Error as error:
            print(f"Ошибка при сохранении кода: {error}")

    async def get_code(self, email):
        try:
            row = await self.fetch_one(
                "SELECT code FROM registration_codes WHERE email = ?", (email,)
            )
            return row[0] if row else None
        except aiosqlite.Error as error:
            print(f"Ошибка при получении кода: {error}")
            return None

    async def get_code_timestamp(self, email):
        try:
            row = await self.fetch_one(
                "SELECT timestamp FROM registration_codes WHERE email = ?", (email,)
            )
            return row[0] if row else None
        except aiosqlite.Error as error:
            print(f"Ошибка при получении времени создания кода: {error}")


db = SqliteSaveCode()
