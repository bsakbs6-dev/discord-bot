import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import config

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


def has_any_role(member: discord.Member, roles: list[int]) -> bool:
    return any(role.id in roles for role in member.roles)


@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Бот запущен как {bot.user}")
    print(f"discord.py {discord.__version__}")

    try:
        synced = await bot.tree.sync()
        print(f"Slash-команд синхронизировано: {len(synced)}")
    except Exception as e:
        print(e)

    print("=" * 40)


bot.run(TOKEN)
