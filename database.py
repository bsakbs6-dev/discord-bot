import aiosqlite
import config

DATABASE = config.DATABASE_NAME


async def init_database():
    async with aiosqlite.connect(DATABASE) as db:

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
            punishment_type TEXT NOT NULL,
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


async def execute(query: str, params=()):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(query, params)
        await db.commit()


async def fetchone(query: str, params=()):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(query, params)

        return await cursor.fetchone()


async def fetchall(query: str, params=()):
    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(query, params)

        return await cursor.fetchall()


# ============================
# Проверки
# ============================

async def add_check(user_id, moderator_id, expires_at):

    await execute(
        """
        INSERT OR REPLACE INTO checks
        (user_id, moderator_id, expires_at)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            moderator_id,
            expires_at
        )
    )


async def remove_check(user_id):

    await execute(
        """
        DELETE FROM checks
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )


async def get_checks():

    return await fetchall(
        """
        SELECT *
        FROM checks
        """
    )


# ============================
# Наказания
# ============================

async def add_punishment(
        user_id,
        moderator_id,
        punishment_type,
        reason,
        expires_at
):

    await execute(
        """
        INSERT INTO punishments
        (
            user_id,
            moderator_id,
            punishment_type,
            reason,
            expires_at
        )
        VALUES
        (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            moderator_id,
            punishment_type,
            reason,
            expires_at
        )
    )


async def remove_punishment(user_id, punishment_type):

    await execute(
        """
        DELETE FROM punishments
        WHERE user_id=?
        AND punishment_type=?
        """,
        (
            user_id,
            punishment_type
        )
    )


async def get_punishments():

    return await fetchall(
        """
        SELECT *
        FROM punishments
        """
    )


# ============================
# Состав
# ============================

async def add_member(
        user_id,
        nickname,
        privilege
):

    await execute(
        """
        INSERT OR REPLACE INTO roster
        VALUES
        (?, ?, ?)
        """,
        (
            user_id,
            nickname,
            privilege
        )
    )


async def remove_member(user_id):

    await execute(
        """
        DELETE FROM roster
        WHERE user_id=?
        """,
        (
            user_id,
        )
    )


async def get_members():

    return await fetchall(
        """
        SELECT *
        FROM roster
        ORDER BY privilege
        """
    )
