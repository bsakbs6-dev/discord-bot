import aiosqlite

DATABASE_NAME = "legionmoder.db"


async def init_database():
    async with aiosqlite.connect(DATABASE_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS checks(
            user_id INTEGER PRIMARY KEY,
            moderator_id INTEGER NOT NULL,
            expires_at INTEGER NOT NULL
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS punishments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            moderator_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            reason TEXT NOT NULL,
            expires_at INTEGER NOT NULL
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS roster(
            user_id INTEGER PRIMARY KEY,
            nickname TEXT NOT NULL,
            privilege TEXT NOT NULL
        )
        """)

        await db.commit()


async def execute(query: str, parameters=()):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute(query, parameters)
        await db.commit()


async def fetchone(query: str, parameters=()):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute(query, parameters)

        row = await cursor.fetchone()

        return row


async def fetchall(query: str, parameters=()):
    async with aiosqlite.connect(DATABASE_NAME) as db:

        cursor = await db.execute(query, parameters)

        rows = await cursor.fetchall()

        return rows
