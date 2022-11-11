import traceback
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from nationstates_bot import NationStatesBot
from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.DAOs.postgresql import Login, Nation
from ns_bot.views.configure import NewNation


class ServerController(BaseNationstateController):
    def __init__(self, bot: NationStatesBot, login_table: Login, nation_table: Nation) -> None:
        super().__init__(bot)
        self.login_table = login_table
        self.nation_table = nation_table

    async def configure(self, interaction: discord.Interaction):
        """TODO add setup for them to add a nation"""
        pass

    async def add_nation(self, interaction: discord.Interaction):
        new_nation_view = NewNation(self.bot.nationstates_api, self.login_table, self.nation_table)
        await interaction.response.send_message(
            "Please log into your existing nation or create a new one",
            view=new_nation_view,
            ephemeral=True,
        )

    async def remove_nation(self, interaction: discord.Interaction, nation: str):
        guild_id = await self.nation_table.get_guild_id(nation=nation)
        if guild_id == interaction.guild_id:
            await self.nation_table.remove_nation(nation=nation)
            await self.login_table.remove_nation(nation=nation)
            await interaction.response.send_message(
                f"{nation} is no longer associated with this server.", ephemeral=True
            )
            return
        await interaction.response.send_message(
            f"{nation} was already not associated with this server.", ephemeral=True
        )
