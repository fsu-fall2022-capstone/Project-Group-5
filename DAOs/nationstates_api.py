from aiohttp import ClientSession


class NationStatesAPI:

    BASE_URL = "https://www.nationstates.net/cgi-bin/api.cgi"

    def __init__(self, web_client: ClientSession) -> None:
        self.web_client = web_client

    async def get_public_nation_data(self, nation: str, shards: list[str]):
        params = {"nation": nation, "q": "+".join(shards)}
        async with self.web_client.get(
            self.BASE_URL,
            headers={'User-Agent': 'NS Discord Bot'},
            params=params,
        ) as response:
            if response.ok:
                return await response.text()


# url = "https://www.nationstates.net/cgi-bin/api.cgi"
# p = {"nation" : "Computer Chip", "q":"policies"}
# h = {'User-Agent': 'Testing for now'}
# a = requests.get(url, headers=h, params=p)
