from ns_bot.DAOs.postgresql.base_sql_table import *


class CommandUsage(BaseSQLTable):
    """
    * command text PRIMARY KEY,
    * usage_count integer
    """

    def __init__(self, db_pool: Pool) -> None:
        super().__init__("command_usage", db_pool)

    @ensure_connection
    async def increment_command(self, *, command: str, con: Optional[Connection] = None):
        await con.execute(
            f"""
            UPDATE {self.TABLE_NAME}
            SET usage_count = usage_count + 1
            WHERE command = $1
            """,
            command,
        )

    @ensure_connection
    async def command_usage_count(self, *, command: str, con: Optional[Connection] = None) -> int:
        return await con.fetchval(
            f"""
            SELECT usage_count from {self.TABLE_NAME} 
            WHERE command = $1
            """,
            command,
        )
