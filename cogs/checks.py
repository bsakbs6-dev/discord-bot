import time

import discord
from discord import app_commands
from discord.ext import commands

import config
import database
import utils


class Checks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="проверка",
        description="Выдать игроку проверку"
    )
    async def check(
        self,
        interaction: discord.Interaction,
        пользователь: discord.Member
    ):

        if not utils.has_any_role(
            interaction.user,
            config.STAFF_ROLES
        ):
            return await interaction.response.send_message(
                "❌ У вас недостаточно прав.",
                ephemeral=True
            )

        role = interaction.guild.get_role(
            config.CHECK_ROLE
        )

        if role is None:
            return await interaction.response.send_message(
                "❌ Не найдена роль проверки.",
                ephemeral=True
            )

        reject_role = interaction.guild.get_role(
            config.REJECT_ROLE
        )

        if role in пользователь.roles:
            return await interaction.response.send_message(
                "❌ Игрок уже находится на проверке.",
                ephemeral=True
            )

        if reject_role and reject_role in пользователь.roles:
            await пользователь.remove_roles(reject_role)

        await пользователь.add_roles(role)

        expires = utils.create_check_timestamp()

        await database.add_check(
            пользователь.id,
            interaction.user.id,
            expires
        )

        embed = utils.log_embed(
            title="🔍 Выдана проверка",
            moderator=interaction.user,
            target=пользователь
        )

        await utils.send_log(
            self.bot,
            embed
        )

        await interaction.response.send_message(
            f"✅ {пользователь.mention} отправлен на проверку."
        )
