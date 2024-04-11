import time
from os import getenv

import aiosqlite
import asyncpg
from dotenv import load_dotenv

from resources import config

load_dotenv()


class SqliteDatabase:
    def __init__(self):
        self.con = None
        self.cur = None

    async def connect(self) -> None:
        try:
            self.con = await aiosqlite.connect(config.sqlite()["name"])
            self.cur = await self.con.cursor()
            if self.con:
                print("SQLite подключился")
            table_save_code = "CREATE TABLE IF NOT EXISTS registration_codes(id INTEGER PRIMARY KEY,email TEXT, " \
                              "code TEXT, timestamp REAL) "
            await self.execute_query(table_save_code)

            await self.con.commit()
        except aiosqlite.Error as error:
            print(f"Ошибка при подключении к базе данных SQLite: {error}")

    async def disconnect(self) -> None:
        if self.con:
            await self.con.close()

    async def execute_query(self, query: str, params=None) -> bool:
        try:
            if not self.con:
                await self.connect()
            if params:
                async with self.con.execute(query, params):
                    pass
            else:
                async with self.con.execute(query):
                    pass
            await self.con.commit()
            return True
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return False

    async def fetch_one(self, query: str, params=None):
        try:
            if not self.con:
                await self.connect()
            if params:
                await self.cur.execute(query, params)
            else:
                await self.cur.execute(query)
            row = await self.cur.fetchone()
            return row
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return None

    async def fetch_all(self, query: str, params=None) -> list:
        try:
            if not self.con:
                await self.connect()
            if params:
                async with self.con.execute(query, params) as cur:
                    result = await cur.fetchall()
            else:
                async with self.con.execute(query) as cur:
                    result = await cur.fetchall()
            return result
        except aiosqlite.Error as error:
            print(f"Ошибка при выполнении запроса SQLite: {error}")
            return []

    async def save_code(self, email, code):
        try:
            await self.execute_query(
                "INSERT OR REPLACE INTO registration_codes (email, code, timestamp) VALUES (?, ?, ?)",
                (email, code, time.time()))
        except aiosqlite.Error as error:
            print(f"Ошибка при сохранении кода: {error}")

    async def get_code(self, email):
        try:
            row = await self.fetch_one("SELECT code FROM registration_codes WHERE email = ?", (email,))
            return row[0] if row else None
        except aiosqlite.Error as error:
            print(f"Ошибка при получении кода: {error}")
            return None

    async def get_code_timestamp(self, email):
        try:
            row = await self.fetch_one("SELECT timestamp FROM registration_codes WHERE email = ?", (email,))
            return row[0] if row else None
        except aiosqlite.Error as error:
            print(f"Ошибка при получении времени создания кода: {error}")


class PostgresqlDatabase:
    def __init__(self):
        self.con = None
        self.cur = None

    async def connect(self) -> None:
        try:
            self.con = await asyncpg.connect(
                user=getenv("postgre_username"),
                password=getenv("postgre_password"),
                database=config.postgresql()["name"],
                host=getenv("postgre_host"),
                port=getenv("postgre_port"),
            )
            self.cur = await self.con.cursor()
            if self.con:
                print("PostgreSQL: подключился")
            table_users = (
                "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, telegram_id TEXT, role TEXT "
                "DEFAULT normal "
            )
            table_black_list = "CREATE TABLE IF NOT EXISTS black_list(command TEXT)"
            await self.execute_query(table_users)
            await self.execute_query(table_black_list)
            await self.con.commit()
        except asyncpg as error:
            print(f"Ошибка при подключении к базе данных PostgreSQL: {error}")

    async def disconnect(self) -> None:
        if self.con:
            await self.con.close()

    async def execute_query(self, query: str, params=None) -> bool:
        try:
            if not self.con:
                await self.connect()
            if params:
                await self.cur.execute(query, params)
            else:
                await self.cur.execute(query)
            await self.con.commit()
            return True
        except asyncpg as error:
            print(f"Ошибка при выполнении запроса PostgreSQL: {error}")
            return False

    async def fetch_all(self, query: str, params=None) -> list:
        try:
            if not self.con:
                await self.connect()
            if params:
                await self.cur.execute(query, params)
            else:
                await self.cur.execute(query)
            return await self.cur.fetchall()
        except asyncpg as error:
            print(f"Ошибка при выполнении запроса PostgreSQL: {error}")
            return []

    async def save_code(self, email, code) -> None:
        pass

    async def get_code(self, email) -> str | None:
        pass

    async def get_code_timestamp(self, email) -> str | None:
        pass


class DataBase:
    def __init__(self, db_type: str):
        self.db_type = db_type.lower()
        if self.db_type == "sqlite":
            self.database = SqliteDatabase()
        elif self.db_type == "postgresql":
            self.database = PostgresqlDatabase()
        else:
            raise ValueError(
                f"{db_type} - неподдерживаемый тип базы данных.\nИспользуйте PostgreSQL или SQLite"
            )

    async def connect(self) -> None:
        await self.database.connect()

    async def disconnect(self) -> None:
        await self.database.disconnect()

    async def save_code(self, email, code) -> None:
        await self.database.save_code(email, code)

    async def get_code(self, email) -> None:
        await self.database.get_code(email)

    async def get_code_timestamp(self, email) -> None:
        await self.database.get_code_timestamp(email)


db = DataBase(db_type=config.database()["type"])
