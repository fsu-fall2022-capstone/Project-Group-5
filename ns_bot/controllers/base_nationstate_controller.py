import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_controller import BaseController


class BaseNationstateController(BaseController):
    @classmethod
    def shard_autocomplete(cls, current: str, valid_shards) -> list[app_commands.Choice[str]]:
        options = [
            app_commands.Choice(name=valid, value=valid)
            for valid in valid_shards
            if current.lower() in valid.lower()
        ]
        options.sort(key=lambda x: x.name)
        return options[:25]
