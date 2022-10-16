import asyncio
import os
from typing import List, Optional

import asyncpg
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

from DAOs.nationstates_api import NationStatesAPI
from utils.logger import Logger

load_dotenv()


class NationStatesBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.base_logger = Logger("bot")

        self.db_pool = db_pool
        self.web_client = web_client

        self.nationstates_api = NationStatesAPI(self.web_client)

        self.testing_guild_id = testing_guild_id

        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # Load in cogs
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # Sync tree with testing guild
        # Only do this to testing guild and not global
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

        self.base_logger.info(
            f"Logged in as: {self.user.name} - {self.user.id}\tVersion: {discord.__version__}"
        )


async def main():

    exts = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            exts.append(f"cogs.{filename[:-3]}")

    async with ClientSession() as web_client, asyncpg.create_pool(
        database="nations", user=os.environ.get("USER"), command_timeout=30
    ) as pool:

        async with NationStatesBot(
            commands.when_mentioned,
            intents=discord.Intents.default(),
            db_pool=pool,
            web_client=web_client,
            initial_extensions=exts,
            # testing_guild_id=1012371257494360115,
        ) as bot:

            await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
