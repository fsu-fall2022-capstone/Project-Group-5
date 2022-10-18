import asyncio
from datetime import datetime
from typing import Optional

from aiohttp import ClientSession


class NationStatesAPI:

    BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"

    def __init__(self, web_client: ClientSession) -> None:
        self.web_client = web_client
        self.__rate_limit = 40
        self.ratelimit_sleep_time = 4
        self.__concurrent_requests__ = 0
        self.__ratelimit_start_time = datetime.now()

    async def get_response(self, headers: dict, params: dict):
        # await self.__rate_limit()
        self.__concurrent_requests__ += 1
        output = None
        async with self.web_client.get(
            self.BASE_URL,
            headers=headers,
            params=params,
        ) as response:
            if response.ok:
                output = await response.text()
        self.__concurrent_requests__ -= 1
        return output

    async def __rate_limit(self):
        # await asyncio.sleep(0.1)
        return

    async def get_public_nation_data(self, nation: str, shards: Optional[list[str]] = None):
        params = {"nation": nation}
        if shards:
            params["q"] = "+".join(shards)
        headers = {'User-Agent': 'NS Discord Bot'}
        return await self.get_response(headers, params)


# url = "https://www.nationstates.net/cgi-bin/api.cgi"
# p = {"nation" : "Computer Chip", "q":"policies"}
# h = {'User-Agent': 'Testing for now'}
# a = requests.get(url, headers=h, params=p)
