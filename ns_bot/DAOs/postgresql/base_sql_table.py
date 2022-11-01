from types import NoneType
from typing import Optional

import asyncpg
from asyncpg import Connection, Pool
from asyncpg.connection import cursor


def ensure_connection(function):
    async def runner(calling_object, *args, **kwargs):
        con = kwargs.get("con", None)
        if type(con) == Connection:
            return await function(calling_object, *args, **kwargs)
        elif type(con) == NoneType:
            async with calling_object.db_pool.acquire() as con:
                kwargs["con"] = con
                return await function(calling_object, *args, **kwargs)

    return runner


class BaseSQLTable:
    def __init__(self, table_name: str, db_pool: Pool) -> None:
        self.TABLE_NAME = table_name
        self.db_pool = db_pool

    @ensure_connection
    async def get_all(self, *, con: Optional[Connection] = None):
        return await con.fetch(f"SELECT * from {self.TABLE_NAME}")

    async def get_batch_of_all(self, *, con: Connection, batch_size: int):
        table_cursor: cursor.Cursor = await self.get_cursor(con=con)
        table_row_count = await self.get_row_count()
        for _ in range(-(-table_row_count // batch_size)):
            yield await table_cursor.fetch(batch_size)

    async def get_cursor(self, *, con: Connection) -> cursor.Cursor:
        return await con.cursor(f"SELECT * from {self.TABLE_NAME}")

    @ensure_connection
    async def get_row_count(self, *, con: Optional[Connection] = None) -> int:
        return await con.fetchval(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
