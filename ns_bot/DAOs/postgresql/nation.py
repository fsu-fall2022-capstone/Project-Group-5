from DAOs.postgresql.base_sql_table import *


class Nation(BaseSQLTable):
    """
    * nation text PRIMARY KEY not null,
    * guild_id bigint not null,
    * vote_time int default -1,
    * vote_channel bigint
    """

    def __init__(self, db_pool: Pool) -> None:
        super().__init__("nation", db_pool)

    @ensure_connection
    async def add_nation(self, *, nation: str, guild_id: int, con: Optional[Connection] = None):
        await con.execute(
            f"""
            insert into {self.TABLE_NAME} (nation, guild_id)
            values ($1, $2)
            """,
            nation,
            guild_id,
        )

    @ensure_connection
    async def update_nation_guild(
        self, *, nation: str, guild_id: int, con: Optional[Connection] = None
    ):
        await self.remove_nation(nation=nation, con=con)
        await self.add_nation(nation=nation, guild_id=guild_id, con=con)

    @ensure_connection
    async def upsert_nation(self, *, nation: str, guild_id: int, con: Optional[Connection] = None):
        if self.nation_already_present(nation=nation, con=con):
            return await con.execute(
                f"""
                UPDATE {self.TABLE_NAME} 
                SET guild_id = $1
                WHERE nation = $2
                """,
                guild_id,
                nation,
            )
        return await con.execute(
            f"""
            insert into {self.TABLE_NAME} (nation, guild_id)
            values ($1, $2)
            """,
            nation,
            guild_id,
        )

    @ensure_connection
    async def nation_already_present(
        self, *, nation: str, con: Optional[Connection] = None
    ) -> bool:
        check = await con.fetchval(
            f"""
            SELECT * from {self.TABLE_NAME} 
            WHERE nation = $1
            """,
            nation,
        )
        return True if check else False

    @ensure_connection
    async def get_guild_id(self, *, nation: str, con: Optional[Connection] = None):
        return await con.fetchval(
            f"""
            SELECT guild_id from {self.TABLE_NAME} 
            WHERE nation = $1
            """,
            nation,
        )

    @ensure_connection
    async def get_vote_time(self, *, nation: str, con: Optional[Connection] = None):
        return await con.fetchval(
            f"""
            SELECT vote_time from {self.TABLE_NAME} 
            WHERE nation = $1
            """,
            nation,
        )

    @ensure_connection
    async def get_vote_channel(self, *, nation: str, con: Optional[Connection] = None):
        return await con.fetchval(
            f"""
            SELECT vote_channel from {self.TABLE_NAME} 
            WHERE nation = $1
            """,
            nation,
        )

    @ensure_connection
    async def update_vote_time(
        self, *, nation: str, vote_time: int, con: Optional[Connection] = None
    ):
        await con.execute(
            f"""
            UPDATE {self.TABLE_NAME} 
            SET vote_time = $1
            WHERE nation = $2
            """,
            vote_time,
            nation,
        )

    @ensure_connection
    async def update_vote_channel(
        self, *, nation: str, vote_channel: int, con: Optional[Connection] = None
    ):
        await con.execute(
            f"""
            UPDATE {self.TABLE_NAME} 
            SET vote_channel = $1
            WHERE nation = $2
            """,
            vote_channel,
            nation,
        )

    @ensure_connection
    async def remove_nation(self, *, nation: str, con: Optional[Connection] = None):
        await con.execute(
            f"""
            DELETE from {self.TABLE_NAME}
            WHERE nation = $1
            """,
            nation,
        )
