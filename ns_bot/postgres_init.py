import asyncio
import os

import asyncpg
from asyncpg import Connection


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
                    password bytea not null,
                    pin text
                )
                """
            )

            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS nation (
                    nation text PRIMARY KEY not null,
                    guild_id bigint not null,
                    vote_time int default -1,
                    vote_channel bigint
                )
                """
            )

            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS live_issues (
                    nation text not null,
                    issue_id int not null,
                    issue_channel bigint not null,
                    start_time timestamp WITH TIME ZONE DEFAULT (current_timestamp AT TIME ZONE 'UTC')
                )
                """
            )

            await con.execute(
                """
                CREATE TABLE IF NOT EXISTS issue_votes (
                    issue_channel bigint not null,
                    voter bigint not null,
                    option int not null
                )
                """
            )


async def main():
    await db_init()
    # await quick_test()


if __name__ == "__main__":
    asyncio.run(main())
