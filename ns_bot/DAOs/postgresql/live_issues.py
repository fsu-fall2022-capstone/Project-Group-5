from ns_bot.DAOs.postgresql.base_sql_table import *


class LiveIssues(BaseSQLTable):
    """
    * nation text not null,
    * issue_id int not null,
    * issue_channel bigint not null,
    * start_time timestamp WITH TIME ZONE DEFAULT (current_timestamp AT TIME ZONE 'UTC')
    """

    def __init__(self, db_pool: Pool) -> None:
        super().__init__("live_issues", db_pool)

    @ensure_connection
    async def get_issue_start_time_and_vote_channel(
        self, *, nation: str, issue_id: int, con: Optional[Connection] = None
    ) -> tuple:
        return await con.fetchval(
            f"""
            SELECT (start_time, issue_channel) from {self.TABLE_NAME}
            WHERE nation = $1 and issue_id = $2
            """,
            nation,
            issue_id,
        )

    @ensure_connection
    async def get_nation_issues(self, *, nation: str, con: Optional[Connection] = None):
        return await con.fetch(
            f"""
            SELECT * from {self.TABLE_NAME} 
            WHERE nation = $1
            """,
            nation,
        )

    @ensure_connection
    async def get_issue_id_from_channel(
        self, *, issue_channel: int, con: Optional[Connection] = None
    ):
        return await con.fetchval(
            f"""
            SELECT issue_id from {self.TABLE_NAME} 
            WHERE issue_channel = $1
            """,
            issue_channel,
        )

    @ensure_connection
    async def insert_issue(
        self, *, nation: str, issue_id: int, issue_channel: int, con: Optional[Connection] = None
    ):
        await con.execute(
            f"""
            INSERT into {self.TABLE_NAME} 
            VALUES ($1, $2, $3)
            """,
            nation,
            issue_id,
            issue_channel,
        )

    @ensure_connection
    async def remove_issue(self, *, nation: str, issue_id: int, con: Optional[Connection] = None):
        await con.execute(
            f"""
            DELETE from {self.TABLE_NAME}
            WHERE nation = $1 and issue_id = $2
            """,
            nation,
            issue_id,
        )
