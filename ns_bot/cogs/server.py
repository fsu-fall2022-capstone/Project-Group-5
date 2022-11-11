import discord
from discord import app_commands
from discord.ext import commands

from nationstates_bot import NationStatesBot
from ns_bot.controllers.server_controller import ServerController
from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.DAOs.postgresql import Login, Nation
from ns_bot.utils.logger import Logger


@app_commands.guild_only()
class Server(commands.Cog):
    """Handle server based nation"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.login_table = Login(self.bot.db_pool)
        self.nation_table = Nation(self.bot.db_pool)

        self.server_controller = ServerController(bot, self.login_table, self.nation_table)

        self.logger = Logger("server")
        self.logger.info("server loaded")

    @app_commands.command(description="Configure your server to host a nation")
    @app_commands.checks.has_permissions(administrator=True)
    async def configure(self, interaction: discord.Interaction):
        await self.server_controller.configure(interaction)

    @app_commands.command(description="Add a nation to this server")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_nation(self, interaction: discord.Interaction):
        await self.server_controller.add_nation(interaction)

    @app_commands.command(description="Remove a nation from this server")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(nation="The name of the nation you would like to remove")
    async def remove_nation(self, interaction: discord.Interaction, nation: str):
        await self.server_controller.remove_nation(interaction, nation)


async def setup(bot: NationStatesBot):
    await bot.add_cog(Server(bot))
