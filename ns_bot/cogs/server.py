from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from nationstates_bot import NationStatesBot
from ns_bot.controllers.server_controller import ServerController
from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.utils.logger import Logger


class Server(commands.Cog):
    """Handle server based nation"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.server_controller = ServerController(bot)

        self.logger = Logger("server")
        self.logger.info("server loaded")


async def setup(bot: NationStatesBot):
    await bot.add_cog(Server(bot))
