import discord

from ns_bot.DAOs.postgresql import IssueVotes, LiveIssues


class VotingDropdown(discord.ui.Select):
    def __init__(
        self, option_amount: int, live_issues_table: LiveIssues, issue_votes_table: IssueVotes
    ):

        options = [discord.SelectOption(label="Ignore Issue", value="-1")]
        for i in range(option_amount):
            options.append(discord.SelectOption(label=f"Option {i + 1}", value=i))

        super().__init__(
            placeholder="Option to vote on",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"issues_select:options",
        )
        self.live_issues_table = live_issues_table
        self.issue_votes_table = issue_votes_table

    async def callback(self, interaction: discord.Interaction):
        issue_id: int = await self.live_issues_table.get_issue_id_from_channel(
            issue_channel=interaction.channel_id
        )
        if not issue_id:
            return await interaction.response.send_message(
                f"This issue has already been voted on", ephemeral=True
            )
        await self.issue_votes_table.user_vote(
            issue_channel=interaction.channel_id,
            user_id=interaction.user.id,
            option=int(self.values[0]),
        )
        clean_option = int(self.values[0]) + 1
        if not clean_option:
            return await interaction.response.send_message(
                f"You voted to skip this issue", ephemeral=True
            )
        await interaction.response.send_message(f"You voted for {clean_option}", ephemeral=True)


class IssueView(discord.ui.View):
    def __init__(
        self, option_amount: int, live_issues_table: LiveIssues, issue_votes_table: IssueVotes
    ):
        super().__init__(timeout=None)

        self.add_item(VotingDropdown(option_amount, live_issues_table, issue_votes_table))
