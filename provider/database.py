import aiosqlite
import pandas as pd
from aiosqlite import Connection
from openpyxl import load_workbook


class ExcelParser:
    @staticmethod
    def parse_excel(excel_path):
        data = {}
        wb = load_workbook(filename=excel_path)
        for sheet in wb.sheetnames:
            df = pd.read_excel(excel_path, sheet_name=sheet)
            data[sheet] = df
        return data


class ScheduleDB:
    @staticmethod
    async def connect_to_db() -> Connection:
        return await aiosqlite.connect("schedule.db")

    async def create_tables(self):
        conn = await self.connect_to_db()
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Groups (
                group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name VARCHAR(50)
            );
        """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Schedule (
                schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INT,
                day_of_week VARCHAR(20),
                FOREIGN KEY (group_id) REFERENCES Groups(group_id)
            );
        """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_id INT,
                subject_name VARCHAR(100),
                start_time TIME,
                end_time TIME,
                location VARCHAR(100),
                FOREIGN KEY (schedule_id) REFERENCES Schedule(schedule_id)
            );
        """
        )
        await conn.commit()
        await conn.close()

    async def get_group(self, group_name):
        conn = await self.connect_to_db()
        cursor = await conn.execute(
            "SELECT group_id FROM Groups WHERE group_name = ?", (group_name,)
        )
        group = await cursor.fetchone()
        await conn.close()
        return group[0] if group else None

    async def create_group(self, group_name):
        conn = await self.connect_to_db()
        cursor = await conn.execute(
            "INSERT INTO Groups (group_name) VALUES (?)", (group_name,)
        )
        await conn.commit()
        last_row_id = cursor.lastrowid
        await conn.close()
        return last_row_id

    async def get_schedule(self, group_id, day_of_week):
        conn = await self.connect_to_db()
        cursor = await conn.execute(
            "SELECT schedule_id FROM Schedule WHERE group_id = ? AND day_of_week = ?",
            (group_id, day_of_week),
        )
        schedule = await cursor.fetchall()
        await conn.close()
        return [row[0] for row in schedule] if schedule else None

    async def create_schedule(self, group_id, day_of_week):
        conn = await self.connect_to_db()
        cursor = await conn.execute(
            "INSERT INTO Schedule (group_id, day_of_week) VALUES (?, ?)",
            (group_id, day_of_week),
        )
        await conn.commit()
        last_row_id = cursor.lastrowid
        await conn.close()
        return last_row_id

    async def add_subject(
        self, schedule_id, subject_name, start_time, end_time, location
    ):
        conn = await self.connect_to_db()
        cursor = await conn.execute(
            """
                INSERT INTO Subjects (schedule_id, subject_name, start_time, end_time, location) 
                VALUES (?, ?, ?, ?, ?)
            """,
            (schedule_id, subject_name, start_time, end_time, location),
        )
        await conn.commit()
        last_row_id = cursor.lastrowid
        await conn.close()
        return last_row_id

    async def get_weekly_schedule_by_group(self, group_name):
        group_id = await self.get_group(group_name)
        days_of_week = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ]
        weekly_schedule = {}
        conn = await self.connect_to_db()
        for day in days_of_week:
            schedule_ids = await self.get_schedule(group_id, day)
            if schedule_ids is not None:
                for schedule_id in schedule_ids:
                    cursor = await conn.execute(
                        """
                        SELECT subject_name, start_time, end_time, location
                        FROM Subjects
                        WHERE schedule_id = ?
                        """,
                        (schedule_id,),
                    )
                    schedule = await cursor.fetchall()
                    if day not in weekly_schedule:
                        weekly_schedule[day] = []
                    weekly_schedule[day].extend(schedule)
        await conn.close()
        return weekly_schedule

    async def insert_data_from_excel(self, excel_path):
        await self.create_tables()
        data = ExcelParser.parse_excel(excel_path)
        conn = await self.connect_to_db()
        for group_name, df in data.items():
            cursor = await conn.execute(
                "INSERT INTO Groups (group_name) VALUES (?)", (group_name,)
            )
            group_id = cursor.lastrowid
            for index, row in df.iterrows():
                day_of_week = row["day_of_week"]
                cursor = await conn.execute(
                    "INSERT INTO Schedule (group_id, day_of_week) VALUES (?, ?)",
                    (group_id, day_of_week),
                )
                schedule_id = cursor.lastrowid
                start_time = row["start_time"]
                end_time = row["end_time"]
                location = row["location"]
                subject_name = row["subject_name"]
                await conn.execute(
                    "INSERT INTO Subjects (schedule_id, subject_name, start_time, end_time, location) VALUES (?, ?, "
                    "?, ?, ?)",
                    (schedule_id, subject_name, start_time, end_time, location),
                )
        await conn.commit()
        await conn.close()


db = ScheduleDB()
