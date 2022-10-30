from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from nationstates_bot import NationStatesBot
from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.utils.logger import Logger


class DM(commands.Cog):
    """Handle DM based nation (play by yourself)"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.logger = Logger("dm")
        self.logger.info("dm loaded")


async def setup(bot: NationStatesBot):
    await bot.add_cog(DM(bot))
