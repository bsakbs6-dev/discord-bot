from __future__ import annotations

import re
import time
from datetime import datetime

TIME_PATTERN = re.compile(r"^(\d+)([smhdwy])$")


def has_role(member, allowed_roles: list[int]) -> bool:
    """
    Проверка, есть ли у пользователя одна из разрешённых ролей.
    """
    return any(role.id in allowed_roles for role in member.roles)


def parse_duration(duration: str) -> int:
    """
    Преобразует:
    5m
    7d
    2h
    1y

    в секунды.
    """

    duration = duration.lower()

    match = TIME_PATTERN.match(duration)

    if not match:
        raise ValueError("Неверный формат времени.")

    value = int(match.group(1))
    unit = match.group(2)

    multipliers = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
        "y": 31536000,
    }

    return value * multipliers[unit]


def unix_after(duration: str) -> int:
    """
    Возвращает Unix Timestamp окончания срока.
    """

    return int(time.time()) + parse_duration(duration)


def now_date() -> str:
    return datetime.now().strftime("%d.%m.%Y")


def now_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def unix_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M")
