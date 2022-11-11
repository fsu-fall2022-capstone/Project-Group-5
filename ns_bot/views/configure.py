import traceback

import discord

from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.DAOs.postgresql import Login, Nation
from ns_bot.utils.encrypt_decrypt import encrypt
from ns_bot.utils.logger import Logger


class LoginDetails(discord.ui.Modal, title="Login"):
    username = discord.ui.TextInput(
        label="Nation name",
        placeholder="Nation...",
    )

    password = discord.ui.TextInput(
        label="Password",
        placeholder="Password...",
        required=False,
    )

    def __init__(
        self,
        *,
        title: str = "Login",
        nationstates_api: NationStatesAPI,
        login_table: Login,
        nation_table: Nation,
    ) -> None:
        super().__init__(title=title)
        self.nationstates_api = nationstates_api
        self.login_table = login_table
        self.nation_table = nation_table

    async def on_submit(self, interaction: discord.Interaction):
        nation = self.username.value

        if await self.nationstates_api.validate_login_details(nation, self.password.value):
            if await self.nation_table.nation_already_present(nation=nation):
                return await interaction.response.send_message(
                    "This nation is already being used in a server. To use it here, please have it removed from the other server",
                    ephemeral=True,
                )

            password = encrypt(self.password.value)
            await self.login_table.add_nation(nation=nation, password=password)

            await self.nation_table.add_nation(nation=nation, guild_id=interaction.guild_id)
            await interaction.response.send_message(
                "Thank you! To configure your nation, please use the configure command",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "The nation name or password was invalid. Please try again", ephemeral=True
            )
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        Logger("error").error(error, exc_info=True)
        await interaction.response.send_message("An internal error has occurred", ephemeral=True)


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
        await interaction.response.send_modal(
            LoginDetails(
                nationstates_api=self.nationstates_api,
                login_table=self.login_table,
                nation_table=self.nation_table,
            )
        )
