from typing import Optional

import discord
from discord import app_commands

from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.data.shards import VALID_PUBLIC_NATION_SHARDS
from ns_bot.formatting.nation_info import FormatNationInfo


class NationController(BaseNationstateController):
    @classmethod
    async def public_nation_shards_autocomplete(
        cls, _: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        return cls.shard_autocomplete(current, VALID_PUBLIC_NATION_SHARDS)

    async def info(
        self, interaction: discord.Interaction, nation: str, shard: Optional[str] = None
    ):
        data = await self.bot.nationstates_api.get_public_nation_data(
            nation, shards=[shard] if shard else None
        )
        await FormatNationInfo.format(nation, shard, data, self.bot, interaction)
