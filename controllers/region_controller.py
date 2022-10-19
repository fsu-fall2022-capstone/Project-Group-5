import traceback
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_nationstate_controller import BaseNationstateController
from controllers.shards import VALID_REGION_SHARDS

class RegionController(BaseNationstateController):
    @classmethod
    async def region_shards_autocomplete(
        cls, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return cls.shard_autocomplete[current,VALID_REGION_SHARDS]

    @classmethod
    async def info(
        self, interaction: discord.Interaction, region: str, shard: Optional[str] = None
    ):
        data = await self.bot.nationstates_api.get_region_data(
            region, shards = [shard] if shard else None
        )
        await interaction.response.send_messag(embed=discord.Embed(title=region,description=data))