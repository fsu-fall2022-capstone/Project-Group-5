from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from nationstates_bot import NationStatesBot
from ns_bot.controllers.nation_controller import NationController
from ns_bot.utils import Logger


class Nation(commands.GroupCog, group_name="nation"):
    """Handle nation requests"""

    __slots__ = ("bot", "nation_controller", "logger")

    def __init__(self, bot: NationStatesBot):
        self.bot = bot
        super().__init__()

        self.nation_controller = NationController(bot)

        self.logger = Logger("nation")
        self.logger.info("nation loaded")

    @app_commands.command(description="Get public information on a nation")
    @app_commands.describe(
        nation="The name of the nation to get info on",
        shard="The type of data you want to look up",
    )
    @app_commands.autocomplete(shard=NationController.public_nation_shards_autocomplete)
    async def info(
        self, interaction: discord.Interaction, nation: str, shard: Optional[str] = None
    ):
        self.logger.info(f"starting to fetch data with {nation = } and {shard = }")
        try:
            await self.nation_controller.info(interaction, nation, shard)
        except Exception as e:
            self.logger.error(e, exc_info=True)
        self.logger.info(f"fetched {shard} for {nation = }")


async def setup(bot: NationStatesBot):
    await bot.add_cog(Nation(bot))
