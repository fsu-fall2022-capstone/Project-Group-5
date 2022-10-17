from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from DAOs.nationstates_api import NationStatesAPI
from nationstates_bot import NationStatesBot
from utils.logger import Logger


class DM(commands.Cog):
    """Handle communication in DMs (play by yourself)"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.logger = Logger("dm")
        self.logger.info("dm loaded")


async def setup(bot: NationStatesBot):
    await bot.add_cog(DM(bot))
