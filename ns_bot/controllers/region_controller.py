from typing import Optional

import discord
from discord import app_commands

from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.data.shards import VALID_REGION_SHARDS
from ns_bot.formatting.region_info import FormatRegionInfo


class RegionController(BaseNationstateController):
    @classmethod
    async def region_shards_autocomplete(
        cls, _: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return cls.shard_autocomplete(current, VALID_REGION_SHARDS)

    async def info(
        self, interaction: discord.Interaction, region: str, shard: Optional[str] = None
    ):
        data = await self.bot.nationstates_api.get_region_data(
            region, shards=[shard] if shard else None
        )
        await FormatRegionInfo.format(region, shard, data, interaction, self.bot)
