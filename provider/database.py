import asyncio

import aiosqlite
import pandas as pd
from openpyxl import load_workbook


class ScheduleDB:
    def __init__(self, db_path="schedule.db"):
        self.db_path = db_path

    async def create_tables(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS Groups (
                    group_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name VARCHAR(50)
                );
            """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS Schedule (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INT,
                    day_of_week VARCHAR(20),
                    FOREIGN KEY (group_id) REFERENCES Groups(group_id)
                );
            """
            )
            await db.execute(
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
            await db.commit()

    async def get_group(self, group_name):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT group_id FROM Groups WHERE group_name = ?", (group_name,)
            )
            group = await cursor.fetchone()
            return group[0] if group else None

    async def create_group(self, group_name):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO Groups (group_name) VALUES (?)", (group_name,)
            )
            await db.commit()
            return cursor.lastrowid

    async def get_schedule(self, group_id, day_of_week):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT schedule_id FROM Schedule WHERE group_id = ? AND day_of_week = ?",
                (
                    group_id,
                    day_of_week,
                ),
            )
            schedule = await cursor.fetchall()
            return [row[0] for row in schedule] if schedule else None

    async def create_schedule(self, group_id, day_of_week):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO Schedule (group_id, day_of_week) VALUES (?, ?)",
                (group_id, day_of_week),
            )
            await db.commit()
            return cursor.lastrowid

    async def add_subject(
        self, schedule_id, subject_name, start_time, end_time, location
    ):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                    INSERT INTO Subjects (schedule_id, subject_name, start_time, end_time, location) 
                    VALUES (?, ?, ?, ?, ?)
                """,
                (schedule_id, subject_name, start_time, end_time, location),
            )
            await db.commit()
            return cursor.lastrowid

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
        for day in days_of_week:
            schedule_ids = await self.get_schedule(group_id, day)
            if schedule_ids is not None:
                for schedule_id in schedule_ids:
                    async with aiosqlite.connect(self.db_path) as db:
                        cursor = await db.execute(
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
        return weekly_schedule

    async def insert_data_from_excel(self, excel_path):
        await self.create_tables()
        wb = load_workbook(filename=excel_path)
        for sheet in wb.sheetnames:
            group_name = sheet
            df = pd.read_excel(excel_path, sheet_name=sheet)
            print(df.head())
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                await cursor.execute(
                    "INSERT INTO Groups (group_name) VALUES (?)", (group_name,)
                )
                group_id = cursor.lastrowid
                for index, row in df.iterrows():
                    day_of_week = row["day_of_week"]
                    await cursor.execute(
                        "INSERT INTO Schedule (group_id, day_of_week) VALUES (?, ?)",
                        (group_id, day_of_week),
                    )
                    schedule_id = cursor.lastrowid
                    start_time = row["start_time"]
                    end_time = row["end_time"]
                    location = row["location"]
                    subject_name = row["subject_name"]
                    await cursor.execute(
                        "INSERT INTO Subjects (schedule_id, subject_name, start_time, end_time, location) VALUES (?, "
                        "?, ?, ?, ?)",
                        (schedule_id, subject_name, start_time, end_time, location),
                    )
                await db.commit()


db = ScheduleDB()
print(asyncio.run(db.get_weekly_schedule_by_group("PO215")))
