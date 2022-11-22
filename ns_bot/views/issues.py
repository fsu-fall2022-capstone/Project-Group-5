import discord


class VotingDropdown(discord.ui.Select):
    def __init__(self, option_amount: int):

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

    async def callback(self, interaction: discord.Interaction):
        # TODO check if still a live message and then add vote to db
        await interaction.response.send_message(
            f"You voted for {self.values[0]} in {interaction.channel.mention}", ephemeral=True
        )


class IssueView(discord.ui.View):
    def __init__(self, option_amount: int):
        super().__init__(timeout=None)

        self.add_item(VotingDropdown(option_amount))
