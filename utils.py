import re
import time
from datetime import datetime

import discord

import config

TIME_PATTERN = re.compile(r"^(\d+)([smhdwy])$")


def has_any_role(member: discord.Member, allowed_roles: list[int]) -> bool:
    """
    Проверка наличия одной из разрешённых ролей.
    """
    return any(role.id in allowed_roles for role in member.roles)


def parse_duration(duration: str) -> int:
    """
    Поддерживает:
    10s
    5m
    2h
    7d
    2w
    1y
    """

    duration = duration.lower()

    match = TIME_PATTERN.match(duration)

    if match is None:
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


def create_timestamp(duration: str) -> int:
    return int(time.time()) + parse_duration(duration)


def create_check_timestamp() -> int:
    return int(time.time()) + config.CHECK_DAYS * 86400


def create_reject_timestamp() -> int:
    return int(time.time()) + config.REJECT_DAYS * 86400


def current_date() -> str:
    return datetime.now().strftime("%d.%m.%Y")


def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def log_embed(
    title: str,
    moderator: discord.Member,
    target: discord.Member,
    reason: str = "-",
    duration: str = "-"
):

    embed = discord.Embed(
        title=title,
        color=0x2F3136,
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
        name="📄 Причина",
        value=reason,
        inline=False
    )

    embed.add_field(
        name="⏳ Срок",
        value=duration,
        inline=True
    )

    embed.add_field(
        name="📅 Дата",
        value=current_date(),
        inline=True
    )

    embed.add_field(
        name="🕒 Время",
        value=current_time(),
        inline=True
    )

    return embed


async def send_log(bot, embed):

    channel = bot.get_channel(config.LOG_CHANNEL_ID)

    if channel is not None:
        await channel.send(embed=embed)
