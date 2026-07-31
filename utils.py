import re
import discord
from datetime import datetime

import config


TIME_REGEX = re.compile(r"^(\d+)([smhdwy])$")


# ==========================
# Проверка ролей
# ==========================

def has_any_role(member: discord.Member, roles: list[int]) -> bool:
    return any(role.id in roles for role in member.roles)


# ==========================
# Парсер времени
# ==========================

def parse_duration(duration: str) -> int:
    """
    5m
    2h
    7d
    3w
    1y
    """

    duration = duration.lower()

    match = TIME_REGEX.match(duration)

    if not match:
        raise ValueError("Неверный формат времени.")

    value = int(match.group(1))
    unit = match.group(2)

    table = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "y": 31536000
    }

    return value * table[unit]


# ==========================
# Красивое время
# ==========================

def now_date():
    return datetime.now().strftime("%d.%m.%Y")


def now_time():
    return datetime.now().strftime("%H:%M:%S")


# ==========================
# Embed логов
# ==========================

def create_log_embed(
        action: str,
        moderator: discord.Member,
        target: discord.Member,
        reason: str = "-",
        duration: str = "-"
):

    embed = discord.Embed(
        title="LegionModer • Лог действия",
        colour=discord.Colour.orange(),
        timestamp=datetime.now()
    )

    embed.add_field(
        name="👤 Игрок",
        value=target.mention,
        inline=False
    )

    embed.add_field(
        name="🛡 Модератор",
        value=moderator.mention,
        inline=False
    )

    embed.add_field(
        name="⚙ Команда",
        value=action,
        inline=False
    )

    embed.add_field(
        name="⏳ Срок",
        value=duration,
        inline=True
    )

    embed.add_field(
        name="📄 Причина",
        value=reason,
        inline=True
    )

    embed.add_field(
        name="📅 Дата",
        value=now_date(),
        inline=True
    )

    embed.add_field(
        name="🕒 Время",
        value=now_time(),
        inline=True
    )

    return embed


# ==========================
# Логирование
# ==========================

async def send_log(bot, embed):

    channel = bot.get_channel(config.LOG_CHANNEL_ID)

    if channel is not None:
        await channel.send(embed=embed)
