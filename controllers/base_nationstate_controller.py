import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_controller import BaseController
from nationstates_bot import NationStatesBot


class BaseNationstateController(BaseController):
    @classmethod
    def shard_autocomplete(
        cls, current: str, valid_shards: tuple[str]
    ) -> list[app_commands.Choice[str]]:
        options = [
            app_commands.Choice(name=valid, value=valid)
            for valid in valid_shards
            if current.lower() in valid.lower()
        ]
        options.sort(key=lambda x: x.name)
        return options[:25]
