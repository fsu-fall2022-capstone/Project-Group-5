from DAOs.postgresql.base_sql_table import *


class Login(BaseSQLTable):
    """
    * nation text PRIMARY KEY not null,
    * password text not null,
    * pin text
    """

    def __init__(self, db_pool: Pool) -> None:
        super().__init__("login", db_pool)

    @ensure_connection
    async def get_nation_login(self, *, nation: str, con: Optional[Connection] = None) -> tuple:
        return await con.fetchval(
            f"""
            SELECT (password, pin) from {self.TABLE_NAME}
            WHERE nation = $1
            """,
            nation,
        )

    @ensure_connection
    async def update_nation_pin(self, *, nation: str, pin: str, con: Optional[Connection] = None):
        await con.execute(
            f"""
            UPDATE {self.TABLE_NAME} 
            SET pin = $1
            WHERE nation = $2
            """,
            pin,
            nation,
        )

    @ensure_connection
    async def update_nation_password(
        self, *, nation: str, password: str, con: Optional[Connection] = None
    ):
        await con.execute(
            f"""
            UPDATE {self.TABLE_NAME} 
            SET password = $1
            WHERE nation = $2
            """,
            password,
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
