import os
import asyncio
import discord

from discord.ext import commands
from dotenv import load_dotenv

import database

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise RuntimeError("Переменная TOKEN не найдена.")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


EXTENSIONS = (
    "cogs.checks",
    "cogs.moderation",
    "cogs.staff",
)


@bot.event
async def on_ready():

    print("=" * 45)
    print(f"LegionModer успешно запущен")
    print(f"Аккаунт : {bot.user}")
    print(f"ID      : {bot.user.id}")
    print(f"Серверов: {len(bot.guilds)}")
    print("=" * 45)


async def load_extensions():

    for extension in EXTENSIONS:

        try:

            await bot.load_extension(extension)

            print(f"[ OK ] {extension}")

        except Exception as error:

            print(f"[FAIL] {extension}")

            print(error)

    synced = await bot.tree.sync()

    print(f"Синхронизировано {len(synced)} Slash-команд.")


async def main():

    await database.init_database()

    async with bot:

        await load_extensions()

        await bot.start(TOKEN)


if __name__ == "__main__":

    asyncio.run(main())
