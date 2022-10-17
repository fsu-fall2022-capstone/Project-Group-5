import asyncio
import os

import asyncpg
from dotenv import load_dotenv


async def db_init():
    async with asyncpg.create_pool(
        database="nations", user=os.environ.get("USER"), command_timeout=60
    ) as pool:
        async with pool.acquire() as con:
            # Command Usage
            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS command_usage (
                    command text PRIMARY KEY,
                    usage_count integer DEFAULT 0
                )
                """
            )


async def populate_table(table: str):
    pass


async def main():
    await db_init()


if __name__ == "__main__":
    asyncio.run(main())
