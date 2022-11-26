import discord
from discord import app_commands
from discord.ext import commands, tasks

from nationstates_bot import NationStatesBot
from ns_bot.controllers.server_controller import ServerController
from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.DAOs.postgresql import IssueVotes, LiveIssues, Login, Nation
from ns_bot.utils import Logger
from ns_bot.views.issues import IssueView


@app_commands.guild_only()
class Server(commands.Cog):
    """Handle server based nation"""

    def __init__(self, bot: NationStatesBot):
        self.bot = bot

        self.login_table = Login(self.bot.db_pool)
        self.nation_table = Nation(self.bot.db_pool)
        self.issues_votes_table = IssueVotes(self.bot.db_pool)
        self.live_issues_table = LiveIssues(self.bot.db_pool)

        self.server_controller = ServerController(
            bot,
            self.login_table,
            self.nation_table,
            self.live_issues_table,
            self.issues_votes_table,
        )

        self.bot.add_view(IssueView(0, self.live_issues_table, self.issues_votes_table))

        self.check_for_issues_loop = self.check_for_issues.start()
        self.ns_data_dump_loop = self.ns_data_dump.start()

        self.logger = Logger("server")
        self.logger.info("server loaded")

    @tasks.loop(minutes=60)
    async def check_for_issues(self):
        self.logger.info("starting issue loop")
        try:
            await self.server_controller.update_live_issues()
            await self.server_controller.fetch_new_issues()
        except Exception as e:
            self.logger.critical(e, exc_info=True)
        self.logger.info("finished issue loop")

    @check_for_issues.before_loop
    async def before_check_for_issues(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=24)
    async def ns_data_dump(self):
        self.logger.info("starting daily dump extraction")
        try:
            await self.server_controller.ns_data_dump()
        except Exception as e:
            self.logger.critical(e, exc_info=True)
        self.logger.info("got daily dump of nations info")

    @app_commands.command(description="Configure the nation on your server")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(nation="The name of the nation you would like to configure")
    async def configure(self, interaction: discord.Interaction, nation: str):
        await self.server_controller.configure_nation(interaction, nation)

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
