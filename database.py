import aiosqlite

DATABASE = "moderation.db"


async def init_db():
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS checks(
            user_id INTEGER PRIMARY KEY,
            moderator_id INTEGER,
            expires_at INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS punishments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            moderator_id INTEGER,
            type TEXT,
            reason TEXT,
            expires_at INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS clan(
            user_id INTEGER PRIMARY KEY,
            nickname TEXT,
            privilege TEXT
        )
        """)

        await db.commit()
