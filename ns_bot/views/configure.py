import discord

from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.DAOs.postgresql import Login, Nation
from ns_bot.utils.encrypt_decrypt import encrypt


class LoginDetails(discord.ui.Modal, title="Feedback"):
    username = discord.ui.TextInput(
        label="Nation name",
        placeholder="Nation...",
    )

    password = discord.ui.TextInput(
        label="Password",
        placeholder="Password...",
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.stop()


class NewNation(discord.ui.View):
    def __init__(self, nationstates_api: NationStatesAPI, login_table: Login, nation_table: Nation):
        super().__init__()
        self.nationstates_api = nationstates_api
        self.login_table = login_table
        self.nation_table = nation_table
        self.add_item(
            discord.ui.Button(
                label="Create a Nation",
                style=discord.ButtonStyle.url,
                url="https://www.nationstates.net/page=create_nation",
            )
        )

    @discord.ui.button(label="Login", style=discord.ButtonStyle.green)
    async def login(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        details = LoginDetails()
        await interaction.response.send_modal(details)
        await details.wait()

        nation = details.username.value

        if await self.nationstates_api.validate_login_details(nation, details.password.value):

            password = encrypt(details.password.value)
            await self.login_table.add_nation(nation=nation, password=password)

            if self.nation_table.nation_already_present(nation=nation):
                return await interaction.followup.send(
                    "This nation is already being used in a server. To use it here, please have it removed from the other server"
                )

            await self.nation_table.add_nation(
                nation=details.username.value, guild_id=interaction.guild_id
            )
            await interaction.followup.send(
                "Thank you! To configure your nation, please use the configure command"
            )
        else:
            await interaction.followup.send(
                "The nation name or password was invalid. Please try again"
            )
