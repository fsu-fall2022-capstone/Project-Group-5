from aiohttp import ClientSession


class NationStatesAPI:
    def __init__(self, web_client: ClientSession) -> None:
        self.web_client = web_client
