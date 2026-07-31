import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from config import (
    BAN_ROLES,
    MUTE_ROLES,
    BAN_ROLE,
    MUTE_ROLE,
    LOG_CHANNEL_ID
)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_role(self, member: discord.Member, roles: list[int]):
        return any(role.id in roles for role in member.roles)

    async def log_action(self, interaction, command_name, target):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="Лог модерации",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )

        embed.add_field(name="Модератор", value=interaction.user.mention, inline=False)
        embed.add_field(name="Игрок", value=target.mention, inline=False)
        embed.add_field(name="Команда", value=command_name, inline=False)

        await channel.send(embed=embed)

    @app_commands.command(name="бан", description="Выдать бан")
    async def ban(
        self,
        interaction: discord.Interaction,
        пользователь: discord.Member,
        длительность: str,
        причина: str
    ):
        if not self.has_role(interaction.user, BAN_ROLES):
            return await interaction.response.send_message(
                "❌ Нет прав.",
                ephemeral=True
            )

        role = interaction.guild.get_role(BAN_ROLE)

        if role:
            await пользователь.add_roles(role)

        await self.log_action(interaction, f"/бан {длительность}", пользователь)

        await interaction.response.send_message(
            f"✅ {пользователь.mention} получил бан на **{длительность}**\nПричина: **{причина}**"
        )

    @app_commands.command(name="мут", description="Выдать мут")
    async def mute(
        self,
        interaction: discord.Interaction,
        пользователь: discord.Member,
        длительность: str,
        причина: str
    ):
        if not self.has_role(interaction.user, MUTE_ROLES):
            return await interaction.response.send_message(
                "❌ Нет прав.",
                ephemeral=True
            )

        role = interaction.guild.get_role(MUTE_ROLE)

        if role:
            await пользователь.add_roles(role)

        await self.log_action(interaction, f"/мут {длительность}", пользователь)

        await interaction.response.send_message(
            f"✅ {пользователь.mention} получил мут на **{длительность}**\nПричина: **{причина}**"
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))
