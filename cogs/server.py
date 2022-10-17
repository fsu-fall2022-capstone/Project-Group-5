from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from controllers.server_controller import ServerController
from DAOs.nationstates_api import NationStatesAPI
from nationstates_bot import NationStatesBot
from utils.logger import Logger


class Server(commands.Cog):
    """Handle server based nation"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.server_controller = ServerController(bot)

        self.logger = Logger("server")
        self.logger.info("server loaded")

    @app_commands.command(description="Get public information on a nation")
    @app_commands.describe(
        nation="The name of the nation to get info on",
        shard="The type of data you want to look up",
    )
    @app_commands.autocomplete(shard=ServerController.public_shards_autocomplete)
    async def info(self, interaction: discord.Interaction, nation: str, shard: str):
        await self.server_controller.info(interaction, nation, shard)
        self.logger.info(f"fetched {shard} for {nation = }")


async def setup(bot: NationStatesBot):
    await bot.add_cog(Server(bot))
