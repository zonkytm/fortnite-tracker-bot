import datetime
import aiosqlite


async def create_db():
    async with aiosqlite.connect("Tracker.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users(
                    user_id TEXT PRIMARY KEY,
                    time_of_the_first_request TEXT
                )
            """)
            await db.commit()


async def add_user(user_id):
    async with aiosqlite.connect("Tracker.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
            user = await cursor.fetchone()

            if not user:
                await cursor.execute("INSERT INTO Users (user_id, time_of_the_first_request) VALUES (?, ?)",
                                     (user_id, datetime.datetime.now().isoformat()))
                await db.commit()


async def get_all_users():
    async with aiosqlite.connect("Tracker.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT user_id FROM Users")
            users = await cursor.fetchall()
            return [user[0] for user in users]
            