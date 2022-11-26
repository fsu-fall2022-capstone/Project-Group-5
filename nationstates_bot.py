import asyncio
import os
from typing import List

import asyncpg
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

import ns_bot.postgres_init as p_init
from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.utils import Logger

load_dotenv()


class NationStatesBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.base_logger = Logger("bot")

        self.db_pool = db_pool
        self.web_client = web_client

        self.nationstates_api = NationStatesAPI(self.web_client, self.db_pool)

        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # Load in cogs
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        self.base_logger.info(
            f"Logged in as: {self.user.name} - {self.user.id}\tVersion: {discord.__version__}"
        )


async def main():
    await p_init.db_init()

    exts = []
    for filename in os.listdir("./ns_bot/cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            exts.append(f"ns_bot.cogs.{filename[:-3]}")

    async with ClientSession() as web_client, asyncpg.create_pool(
        database="nations", user=os.environ.get("USER"), command_timeout=30
    ) as pool:

        async with NationStatesBot(
            commands.when_mentioned,
            intents=discord.Intents.default(),
            db_pool=pool,
            web_client=web_client,
            initial_extensions=exts,
        ) as bot:
            await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
