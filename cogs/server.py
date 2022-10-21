from dis import disco
from typing import Literal, Optional, List
import aiohttp

import discord
from controllers.server_controller import ServerController
from DAOs.nationstates_api import NationStatesAPI
from discord import app_commands
from discord.ext import commands
from nationstates_bot import NationStatesBot
from utils.logger import Logger


class Server(commands.Cog):
    """Handle server based nation"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.server_controller = ServerController(bot)

        self.logger = Logger("server")
        self.logger.info("server loaded")  

    @app_commands.command(name="shards")
    @app_commands.describe(
        nation ="Name of the nation to be targeted",
        shards ="List of shards to find"
        )
    async def fetch_shards(
        self,
        interaction: discord.Interaction,
        nation: str,
        shards: str,
        ):
        async with NationStatesAPI as session:
            async with session.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}') as resp:
                await interaction.response.send_message(await resp.text() )


async def setup(bot: NationStatesBot):
    await bot.add_cog(Server(bot))
