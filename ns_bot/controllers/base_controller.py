import os

import discord
from discord import app_commands

from nationstates_bot import NationStatesBot


class BaseController:
    __slots__ = ("bot",)

    def __init__(self, bot: NationStatesBot) -> None:
        self.bot = bot

    @staticmethod
    def is_owner():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == int(os.environ.get("OWNER_ID"))

        return app_commands.check(predicate)
