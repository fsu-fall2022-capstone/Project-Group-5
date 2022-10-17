import traceback
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_nationstate_controller import BaseNationstateController


class ServerController(BaseNationstateController):
    async def info(self, interaction: discord.Interaction, nation: str, shard: str):
        data = await self.bot.nationstates_api.get_public_nation_data(nation, shards=[shard])
        await interaction.response.send_message(embed=discord.Embed(title=nation, description=data))
