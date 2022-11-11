import asyncio
import os

import asyncpg
from asyncpg import Connection
from dotenv import load_dotenv


async def db_init():
    async with asyncpg.create_pool(
        database="nations", user=os.environ.get("USER"), command_timeout=60
    ) as pool:
        con: Connection
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

            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS login (
                    nation text PRIMARY KEY not null,
                    password text not null,
                    pin text
                )
                """
            )

            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS nation (
                    nation text PRIMARY KEY not null,
                    id bigint not null,
                    dm bool not null,
                    vote_time int default -1,
                    vote_channel bigint
                )
                """
            )


async def quick_test():
    pass


async def populate_table(table: str):
    pass


async def main():
    await db_init()
    # await quick_test()


if __name__ == "__main__":
    asyncio.run(main())
