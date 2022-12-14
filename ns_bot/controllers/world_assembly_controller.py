from typing import Optional

import discord
from discord import app_commands

from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.data.shards import (
    SPECIAL_WORLD_ASSEMBLY_SHARDS,
    VALID_WORLD_ASSEMBLY_SHARDS,
)
from ns_bot.formatting.world_assembly_info import FormatWAInfo


class WorldAssemblyController(BaseNationstateController):
    @classmethod
    async def wa_shards_autocomplete(
        cls, _: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return cls.shard_autocomplete(current, VALID_WORLD_ASSEMBLY_SHARDS)

    async def info(
        self,
        interaction: discord.Interaction,
        council: app_commands.Choice[int],
        shard: Optional[str] = None,
    ):
        shards = [shard] if shard else None
        if shard.lower() in SPECIAL_WORLD_ASSEMBLY_SHARDS:
            shards.append("resolution")
        data = await self.bot.nationstates_api.get_wa_data(council.value, shards=shards)
        await FormatWAInfo.format(council.name, shard, data, interaction)
