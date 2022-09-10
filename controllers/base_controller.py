import os

import discord
from discord import app_commands
from discord.ext import commands

from graduation_tracker_bot import GraduationBot


class BaseController:
    def __init__(self, bot: GraduationBot) -> None:
        self.bot = bot

    @staticmethod
    def is_owner():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == int(os.environ.get("OWNER_ID"))

        return app_commands.check(predicate)
