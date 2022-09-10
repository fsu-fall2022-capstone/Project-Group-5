import os
import traceback
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_controller import BaseController


class ConfigController(BaseController):
    async def load(self, interaction: discord.Interaction, cog: str):
        if not self.verify_file(cog):
            return await interaction.response.send_message(
                f"Please enter a valid cog\n```json\n{self.bot.cogs}\n```", ephemeral=True
            )
        else:
            try:
                await self.bot.load_extension(f"cogs.{cog}")
                return await interaction.response.send_message(f"Loaded {cog}", ephemeral=True)
            except Exception:
                return await interaction.response.send_message(
                    f"Failed to load\n{traceback.format_exc()}",
                    ephemeral=True,
                )

    async def unload(self, interaction: discord.Interaction, cog: str):
        if not self.verify_file(cog):
            return await interaction.response.send_message(
                f"Please enter a valid cog\n```json\n{self.bot.cogs}\n```", ephemeral=True
            )
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            return await interaction.response.send_message(f"Unloaded {cog}", ephemeral=True)
        except Exception:
            return await interaction.response.send_message(
                f"Failed to unload\n{traceback.format_exc()}", ephemeral=True
            )

    async def reload(self, interaction: discord.Interaction, cog: str = None):
        if cog and not self.verify_file(cog):
            return await interaction.response.send_message(
                f"Please enter a valid cog\n```json\n{self.bot.cogs}\n```", ephemeral=True
            )

        cogs = self.get_cogs(cog)
        reloaded_cogs = []
        try:
            for cog in cogs:
                await self.bot.unload_extension(f"cogs.{cog}")
                await self.bot.load_extension(f"cogs.{cog}")
                reloaded_cogs.append(cog)
            return await interaction.response.send_message(
                f"Reloaded {reloaded_cogs}", ephemeral=True
            )
        except Exception:
            return await interaction.response.send_message(
                f"Failed to reload all\nReloaded {reloaded_cogs}\n{traceback.format_exc()}",
                ephemeral=True,
            )

    async def sync(self, interaction: discord.Interaction, option: Literal["Global", "Guild"]):
        guild = interaction.guild if option == "Guild" else None
        await self.bot.tree.sync(guild=guild)

    @staticmethod
    def verify_file(cog_name: str):
        return os.path.exists(f"./cogs/{cog_name.lower()}.py") and not cog_name.startswith("_")

    @staticmethod
    def get_cogs(cog_name: str = None) -> list[str]:
        if cog_name:
            return [cog_name]
        else:
            return [
                ext[:-3]
                for ext in os.listdir("./cogs/")
                if ext.endswith(".py") and not ext.startswith("_")
            ]


async def cog_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    cogs: list[str] = ConfigController.get_cogs()
    return [
        app_commands.Choice(name=cog, value=cog) for cog in cogs if current.lower() in cog.lower()
    ]
