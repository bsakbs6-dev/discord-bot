import discord
import aiosqlite

from discord.ext import commands
from discord import app_commands

import config
from utils import has_role, unix_after, now_date, now_time


class Checks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="проверка",
        description="Выдать пользователю проверку"
    )
    async def check(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        if not has_role(interaction.user, config.STAFF_ROLES):
            await interaction.response.send_message(
                "❌ Недостаточно прав.",
                ephemeral=True
            )
            return

        role = interaction.guild.get_role(config.CHECK_ROLE)

        if role is None:
            await interaction.response.send_message(
                "❌ Роль проверки не найдена.",
                ephemeral=True
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                "❌ Игрок уже находится на проверке.",
                ephemeral=True
            )
            return

        await member.add_roles(role)

        expires = unix_after("7d")

        async with aiosqlite.connect("moderation.db") as db:

            await db.execute(
                """
                INSERT OR REPLACE INTO checks
                VALUES (?, ?, ?)
                """,
                (
                    member.id,
                    interaction.user.id,
                    expires
                )
            )

            await db.commit()

        embed = discord.Embed(
            title="🔍 Проверка выдана",
            color=0x2ECC71
        )

        embed.add_field(
            name="Игрок",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="Модератор",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="Дата",
            value=now_date(),
            inline=True
        )

        embed.add_field(
            name="Время",
            value=now_time(),
            inline=True
        )

        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel:
            await channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ {member.mention} отправлен на проверку."
        )


async def setup(bot):
    await bot.add_cog(Checks(bot))
