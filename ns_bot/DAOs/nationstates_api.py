import asyncio
from datetime import datetime
from typing import Optional

import asyncpg
from aiohttp import ClientSession

from ns_bot.DAOs.postgresql import Login


def ratelimit(function):
    async def runner(calling_object, *args, **kwargs):
        await calling_object._rate_limit()
        calling_object.__concurrent_requests__ += 1
        output = await function(calling_object, *args, **kwargs)
        calling_object.__concurrent_requests__ -= 1
        return output

    return runner


class NationStatesAPI:
    USER_AGENT = "NS Discord Bot"
    BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"

    def __init__(self, web_client: ClientSession, db_pool: asyncpg.Pool) -> None:
        self.web_client = web_client
        self.__rate_limit__ = 40
        self.ratelimit_sleep_time = 4
        self.__concurrent_requests__ = 0
        self.__ratelimit_start_time = datetime.now()

        self.login_table = Login(db_pool)

    @ratelimit
    async def get_response(self, headers: dict, params: dict):
        output = None
        async with self.web_client.get(
            self.BASE_URL,
            headers=headers,
            params=params,
        ) as response:
            if response.ok:
                output = await response.text()
        return output

    async def get_x_data(self, type: str, type_value: str, shards: Optional[list[str]] = None):
        params = {type: type_value}
        if shards:
            params["q"] = "+".join(shards)
        headers = {"User-Agent": self.USER_AGENT}
        return await self.get_response(headers, params)

    async def get_public_nation_data(self, nation: str, shards: Optional[list[str]] = None):
        return await self.get_x_data("nation", nation, shards)

    async def get_region_data(self, region: str, shards: Optional[list[str]] = None):
        return await self.get_x_data("region", region, shards)

    async def get_wa_data(self, council: int, shards: Optional[list[str]] = None):
        return await self.get_x_data("wa", council, shards)

    @ratelimit
    async def validate_login_details(self, nation: str, password: str):
        async with self.web_client.get(
            self.BASE_URL,
            headers={"User-Agent": self.USER_AGENT, "X-password": password},
            params={"nation": nation, "q": "ping"},
        ) as response:
            if pin := response.headers.get("X-Pin"):
                await self.login_table.update_nation_pin(nation=nation, pin=pin)

            return response.ok

    async def get_nation_issues(self, nation: str):
        password, pin = await self.login_table.get_nation_login(nation=nation)
        async with self.web_client.get(
            self.BASE_URL,
            headers={"User-Agent": self.USER_AGENT, "X-password": password, "X-Pin": pin},
            params={"nation": nation, "q": "issues"},
        ) as response:
            if pin := response.headers.get("X-Pin"):
                await self.login_table.update_nation_pin(nation=nation, pin=pin)

            return response.text()

    async def _rate_limit(self):
        # await asyncio.sleep(0.1)
        return


# url = "https://www.nationstates.net/cgi-bin/api.cgi"
# p = {"nation" : "Computer Chip", "q":"policies"}
# h = {'User-Agent': 'Testing for now'}
# a = requests.get(url, headers=h, params=p)
