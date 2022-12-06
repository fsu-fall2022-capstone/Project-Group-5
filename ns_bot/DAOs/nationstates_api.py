import asyncio
from datetime import datetime
from io import BytesIO
from typing import Optional

import asyncpg
from aiohttp import ClientResponse, ClientSession
from PIL import Image

from ns_bot.DAOs.postgresql import Login
from ns_bot.utils import decrypt


def ratelimit(function):
    async def runner(calling_object, *args, **kwargs):
        await calling_object._rate_limit()
        calling_object._concurrent_requests_ += 1
        output = await function(calling_object, *args, **kwargs)
        return output

    return runner


class NationStatesAPI:
    USER_AGENT = "NS Discord Bot"
    BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"
    BASE_IMAGE_URL = "https://www.nationstates.net/images/"

    def __init__(self, web_client: ClientSession, db_pool: asyncpg.Pool) -> None:
        self.web_client = web_client
        self._rate_limit_ = 40
        self.ratelimit_period = 30
        self._concurrent_requests_ = 0
        self.__ratelimit_start_time = datetime.now()

        self.login_table = Login(db_pool)

    @staticmethod
    def auto_authenticate(func):
        @ratelimit
        async def authenticator(cls, *args, **kwargs):
            nation = kwargs.get("nation")

            if login_info := await cls.login_table.get_nation_login(nation=nation):
                password, pin = login_info
                password = decrypt(password)
                kwargs["password"] = password
                kwargs["pin"] = pin or ""

            response: ClientResponse
            response, output = await func(cls, *args, **kwargs)

            if pin := response.headers.get("X-Pin"):
                await cls.login_table.update_nation_pin(nation=nation, pin=pin)
            return output

        return authenticator

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

    @auto_authenticate
    async def validate_login_details(self, *, nation: str, password: str, **kwargs):
        async with self.web_client.get(
            self.BASE_URL,
            headers={"User-Agent": self.USER_AGENT, "X-password": password},
            params={"nation": nation, "q": "ping"},
        ) as response:
            return response, response.ok

    @auto_authenticate
    async def get_nation_issues(self, *, nation: str, password="", pin=""):
        async with self.web_client.get(
            self.BASE_URL,
            headers={"User-Agent": self.USER_AGENT, "X-password": password, "X-Pin": pin or ""},
            params={"nation": nation, "q": "issues"},
        ) as response:
            return response, await response.text()

    @auto_authenticate
    async def respond_to_issue(
        self, *, nation: str, issue_id: int, option: int, password="", pin=""
    ):
        async with self.web_client.get(
            self.BASE_URL,
            headers={"User-Agent": self.USER_AGENT, "X-password": password, "X-Pin": pin or ""},
            params={"nation": nation, "c": "issue", "issue": issue_id, "option": option},
        ) as response:
            return response, await response.text()

    @ratelimit
    async def get_nation_dump(self):
        URL = "https://www.nationstates.net/pages/nations.xml.gz"
        headers = {"User-Agent": self.USER_AGENT}
        async with self.web_client.get(URL, headers=headers) as response:
            return await response.content.read()

    @ratelimit
    async def get_image(self, url: str):
        async with self.web_client.get(url, headers={"User-Agent": self.USER_AGENT}) as response:
            return Image.open(BytesIO(await response.content.read()))

    async def get_banner(self, banner: str):
        return await self.get_image(url=self.BASE_IMAGE_URL + banner)

    async def get_banners(self, banners: list[str]):
        return [await self.get_banner(banner) for banner in banners]

    async def _rate_limit(self):
        time_delta = datetime.now() - self.__ratelimit_start_time
        if time_delta.seconds > self.ratelimit_period:
            self.__ratelimit_start_time = datetime.now()
            self._concurrent_requests_ = 0
        elif self._concurrent_requests_ >= self._rate_limit_:
            await asyncio.sleep(self.ratelimit_period - time_delta.seconds)


# url = "https://www.nationstates.net/cgi-bin/api.cgi"
# p = {"nation" : "Computer Chip", "q":"policies"}
# h = {'User-Agent': 'Testing for now'}
# a = requests.get(url, headers=h, params=p)
