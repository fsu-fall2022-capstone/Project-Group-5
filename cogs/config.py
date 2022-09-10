from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from controllers.config_controller import ConfigController, cog_autocomplete
from graduation_tracker_bot import GraduationBot
from utils.logger import Logger


class Config(commands.Cog):
    def __init__(self, bot: GraduationBot):
        self.bot = bot
        self.config_controller = ConfigController(bot)

        self.logger = Logger("config")
        self.logger.info("config loaded")

    @app_commands.command(description="Log the bot out of discord")
    @ConfigController.is_owner()
    async def logout(self, interaction: discord.Interaction):
        await interaction.response.send_message("Logging off. Goodbye!", ephemeral=True)
        self.logger.info("Logged out")
        await self.bot.close()

    @app_commands.command(description="Load in a cog")
    @app_commands.autocomplete(cog=cog_autocomplete)
    @ConfigController.is_owner()
    async def load(self, interaction: discord.Interaction, cog: str):
        self.logger.info(f"Attempting to load {cog}")
        await self.config_controller.load(interaction, cog)
        self.logger.info(f"Loaded {cog}")

    @app_commands.command(description="Unload one of the bots cogs")
    @app_commands.autocomplete(cog=cog_autocomplete)
    @ConfigController.is_owner()
    async def unload(self, interaction: discord.Interaction, cog: str):
        self.logger.info(f"Attempting to unload {cog}")
        await self.config_controller.unload(interaction, cog)
        self.logger.info(f"Unloaded {cog}")

    @app_commands.command(description="Reload all/one of the bots cogs")
    @app_commands.autocomplete(cog=cog_autocomplete)
    @ConfigController.is_owner()
    async def reload(self, interaction: discord.Interaction, cog: Optional[str] = None):
        self.logger.info(f"Reloading cogs ... ")
        await self.config_controller.reload(interaction, cog)
        self.logger.info(f"Reloaded cogs")

    @app_commands.command(description="Sync slash commands to discord")
    @ConfigController.is_owner()
    async def sync(self, interaction: discord.Interaction, option: Literal["Global", "Guild"]):
        await self.config_controller.sync(interaction, option)
        self.logger.info(f"Synced commands to {option}")


async def setup(bot: GraduationBot):
    await bot.add_cog(Config(bot))
