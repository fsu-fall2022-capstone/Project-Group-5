from typing import Optional

from asyncpg import Connection, Pool

from ns_bot.DAOs.postgresql.base_sql_table import BaseSQLTable, ensure_connection


class IssueVotes(BaseSQLTable):
    """
    * issue_channel bigint not null,
    * voter bigint not null,
    * option int not null
    """

    def __init__(self, db_pool: Pool) -> None:
        super().__init__("issue_votes", db_pool)

    @ensure_connection
    async def get_votes_for_issue(self, *, issue_channel: int, con: Optional[Connection] = None):
        return await con.fetch(
            f"""
            SELECT option from {self.TABLE_NAME}
            WHERE issue_channel = $1
            """,
            issue_channel,
        )

    @ensure_connection
    async def remove_issue(self, *, issue_channel: int, con: Optional[Connection] = None):
        await con.execute(
            f"""
            DELETE from {self.TABLE_NAME}
            WHERE issue_channel = $1
            """,
            issue_channel,
        )

    @ensure_connection
    async def user_vote(
        self, *, issue_channel: int, user_id: int, option: str, con: Optional[Connection] = None
    ):
        if not await self.get_user_vote_on_issue(user_id=user_id, issue_channel=issue_channel):
            return await con.execute(
                f"""
                INSERT into {self.TABLE_NAME}
                VALUES ($1, $2, $3)
                """,
                issue_channel,
                user_id,
                option,
            )

        return await con.execute(
            f"""
            UPDATE {self.TABLE_NAME} SET
            option = $1
            WHERE issue_channel = $2 and voter = $3
            """,
            option,
            issue_channel,
            user_id,
        )

    @ensure_connection
    async def get_user_vote_on_issue(
        self, *, user_id: int, issue_channel: int, con: Optional[Connection] = None
    ):
        return await con.fetchrow(
            f"SELECT * from {self.TABLE_NAME} where voter = $1 and issue_channel = $2",
            user_id,
            issue_channel,
        )
