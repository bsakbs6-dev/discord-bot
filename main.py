import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"✅ Бот запущен как {bot.user}")
    print(f"ID: {bot.user.id}")
    print("=" * 40)


async def load_extensions():
    extensions = [
        "cogs.moderation",
        "cogs.checks",
        "cogs.staff",
    ]

    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Загружен модуль {extension}")
        except Exception as e:
            print(f"❌ Ошибка загрузки {extension}")
            print(e)

    try:
        synced = await bot.tree.sync()
        print(f"✅ Синхронизировано {len(synced)} slash-команд")
    except Exception as e:
        print("❌ Ошибка синхронизации команд")
        print(e)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
