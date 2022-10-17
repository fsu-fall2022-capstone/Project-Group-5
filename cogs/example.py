from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from nationstates_bot import NationStatesBot
from utils.logger import Logger


class Example(commands.Cog):
    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.logger = Logger("example")
        self.logger.info("example loaded")

    @app_commands.command(description="example of things")
    @app_commands.describe(
        pick="An enumerator list to pick from",
        string="A string to echo back",
        number="How many times to repeat the string",
    )
    async def example(
        self,
        interaction: discord.Interaction,
        pick: Literal["A", "B", "C"],
        string: str,
        number: Optional[int] = 1,
    ):
        await interaction.response.send_message(f"You picked {pick} and said : {string * number}")


async def setup(bot: NationStatesBot):
    await bot.add_cog(Example(bot))
