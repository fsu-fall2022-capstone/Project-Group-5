import traceback
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_nationstate_controller import BaseNationstateController
from controllers.shards import VALID_PUBLIC_NATION_SHARDS


class NationController(BaseNationstateController):
    @classmethod
    async def public_nation_shards_autocomplete(
        cls, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return cls.shard_autocomplete(current, VALID_PUBLIC_NATION_SHARDS)

    async def info(
        self, interaction: discord.Interaction, nation: str, shard: Optional[str] = None
    ):
        data = await self.bot.nationstates_api.get_public_nation_data(
            nation, shards=[shard] if shard else None
        )
        await interaction.response.send_message(embed=discord.Embed(title=nation, description=data))
