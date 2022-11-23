import datetime

import discord

from nationstates_bot import NationStatesBot
from ns_bot.controllers.base_nationstate_controller import BaseNationstateController
from ns_bot.DAOs.postgresql import IssueVotes, LiveIssues, Login, Nation
from ns_bot.views.configure import ConfigureNation, NewNation
from ns_bot.views.issues import IssueView


class ServerController(BaseNationstateController):
    def __init__(
        self,
        bot: NationStatesBot,
        login_table: Login,
        nation_table: Nation,
        live_issues_table: LiveIssues,
        issue_votes_table: IssueVotes,
    ) -> None:
        super().__init__(bot)
        self.login_table = login_table
        self.nation_table = nation_table
        self.live_issues_table = live_issues_table
        self.issue_votes_table = issue_votes_table

    async def add_nation(self, interaction: discord.Interaction):
        new_nation_view = NewNation(self.bot.nationstates_api, self.login_table, self.nation_table)
        await interaction.response.send_message(
            "Please log into your existing nation or create a new one\
            \nLog in at your own risk. We store an encrypted version of your information, but even so,\
            please understand the risks associated with sharing your login information",
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

    async def configure_nation(self, interaction: discord.Interaction, nation: str):
        guild_id = await self.nation_table.get_guild_id(nation=nation)
        if interaction.guild.id != guild_id:
            return await interaction.response.send_message(
                f"{nation} is not associated with this server", ephemeral=True
            )

        await interaction.response.send_message(
            "Please select how long each voting period should be. And what channel issues should appear in.",
            ephemeral=True,
            view=ConfigureNation(nation, self.nation_table),
        )

    async def generate_issue(
        self,
        nation: str,
        currency: str,
        article_title: str,
        banner_1: str,
        banner_2: str,
        flag: str,
        issue_number: str,
    ):
        # TODO Remove temp things :
        """
        issue_id from xml
        image should be from newspaper generator
        option_amount = len(xml.option)
        """
        issue_channel = self.bot.get_channel(
            await self.nation_table.get_vote_channel(nation=nation)
        )
        # file = discord.File("path/to/my/image.png", filename="image.png")
        # embed = discord.Embed()
        # embed.set_image(url="attachment://image.png")
        # await channel.send(file=file, embed=embed)
        issue_embed = discord.Embed(title="Reporting for (Jury) Duty")
        issue_embed.set_image(url="https://www.nationstates.net/images/newspaper/i7-1.jpg")

        msg = await issue_channel.send(embed=issue_embed)
        thd = await issue_channel.create_thread(name=f"{nation} Issue #issue_id", message=msg)

        issue_amount = 3
        embeds = [
            discord.Embed(
                title=f"Option {i + 1}",
                description="""TODO get the next issue we are going to send and fill out the options here""",
            )
            for i in range(issue_amount)
        ]

        await thd.send(embeds=embeds, view=IssueView(issue_amount))

    async def fetch_new_issues(self):
        for nation in await self.nation_table.get_all():
            issues = await self.bot.nationstates_api.get_nation_issues(nation["nation"])
            # loop through the issues and check if a new one is present
            # or make another db (or edit current) to store the time till nation has new issue

    async def update_live_issues(self):
        # TODO optimize the search
        # right now the db is called to fetch the vote time for every issue
        # but this can be simplified by ordering/grouping by nation (same time for each issue for each nation)
        data = await self.live_issues_table.get_all()
        for issue in data:
            time_difference: datetime.timedelta = issue["start_time"] - datetime.datetime.utcnow()
            vote_time = self.nation_table.get_vote_time(nation=issue["nation"])
            if vote_time == -1:
                if time_difference.seconds > (datetime.timedelta(seconds=3600 * 24)):
                    await self.send_issue_option(issue, False)
            elif time_difference.seconds > (datetime.timedelta(seconds=3600 * vote_time)):
                await self.send_issue_option(issue, True)

    async def send_issue_option(self, issue: dict, respond_to_api: bool):
        votes = await self.issue_votes_table.get_votes_for_issue(
            issue_channel=issue["issue_channel"]
        )
        option = max(set(votes), key=votes.count) if votes else -1
        nation = issue["nation"]
        issue_id = issue["issue_id"]
        channel: discord.TextChannel = self.bot.get_channel(issue["issue_channel"])
        if option == -1:
            issue_response_result = "The server voted to dismiss this option"
        else:
            issue_response_result = f"The server voted for option {option + 1}\n"

        if respond_to_api:
            # TODO format the response from the API
            issue_response_result += await self.bot.nationstates_api.respond_to_issue(
                nation, issue_id, option
            )

        await channel.send(issue_response_result)
        await self.live_issues_table.remove_issue(nation=nation, issue_id=issue_id)
        await self.issue_votes_table.remove_issue(issue_channel=channel)

    # async def data_dump(self):
    #     # TODO implement a fetch of the nation data dump for things like
    #     # flags to limit calls to API
    #     # data_dict = xmltodict.parse(data_dump_from_ns)
    #     data_dict = {}
    #     nations = data_dict["NATIONS"]["NATION"]
