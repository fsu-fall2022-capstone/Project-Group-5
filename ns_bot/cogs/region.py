from typing import Literal, Optional

import discord
from controllers.region_controller import RegionController
from discord import app_commands
from discord.ext import commands
from nationstates_bot import NationStatesBot
from utils.logger import Logger


class Region(commands.GroupCog, group_name="region"):
    """Handle region requests"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot
        super().__init__()

        self.region_controller = RegionController(bot)

        self.logger = Logger("region")
        self.logger.info("region loaded")

    @app_commands.command(description="Get information on a region")
    @app_commands.describe(
        region="The name of the region to get info on",
        shard="The type of data you want to look up",
    )
    @app_commands.autocomplete(shard=RegionController.region_shards_autocomplete)
    async def info(
        self, interaction: discord.Interaction, region: str, shard: Optional[str] = None
    ):
        self.logger.info(f"starting to fetch data with {region = } and {shard = }")
        await self.region_controller.info(interaction, region, shard)
        self.logger.info(f"fetched {shard} for {region = }")


async def setup(bot: NationStatesBot):
    await bot.add_cog(Region(bot))
