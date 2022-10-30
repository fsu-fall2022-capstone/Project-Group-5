import traceback
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands
from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.data.shards import (
    SPECIAL_WORLD_ASSEMBLY_SHARDS,
    VALID_WORLD_ASSEMBLY_SHARDS,
)


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
        # TODO make stats about the returned info. Because the data will be too large otherwise
        # TODO explore and fix issue with large response just not showing anything
        await interaction.response.send_message(
            embed=discord.Embed(title=council.name, description=data)
        )
