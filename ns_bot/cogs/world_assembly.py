from typing import Literal, Optional

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from nationstates_bot import NationStatesBot
from ns_bot.controllers.world_assembly_controller import WorldAssemblyController
from ns_bot.utils import Logger


class WorldAssembly(commands.GroupCog, group_name="wa"):
    """Handle World Assembly requests"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot
        super().__init__()

        self.world_assembly_controller = WorldAssemblyController(bot)

        self.logger = Logger("world_assembly")
        self.logger.info("world_assembly loaded")

    @app_commands.command(description="Get information on the world assembly")
    @app_commands.describe(
        council="The council to get info on",
        shard="The type of data you want to look up",
    )
    @app_commands.choices(
        council=[
            Choice(name="General Assembly", value=1),
            Choice(name="Security Council", value=2),
        ]
    )
    @app_commands.autocomplete(shard=WorldAssemblyController.wa_shards_autocomplete)
    async def info(
        self,
        interaction: discord.Interaction,
        council: Choice[int],
        shard: Optional[str] = None,
    ):
        self.logger.info(f"starting to fetch data with {council.name = } and {shard = }")
        await self.world_assembly_controller.info(interaction, council, shard)
        self.logger.info(f"fetched {shard} for {council.name = }")


async def setup(bot: NationStatesBot):
    await bot.add_cog(WorldAssembly(bot))
