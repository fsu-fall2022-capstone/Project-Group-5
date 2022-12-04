import xml.etree.ElementTree as ET

from ns_bot.utils.wrappers import async_wrapper


class Formatter:
    BASE_BANNER_URL = "https://www.nationstates.net/images/banners/"
    IMAGE_LIMIT = 10

    async_xml_parse = async_wrapper(ET.fromstring)

    def clean_data(self, data: str):
        return data.replace("&quot;", '"').replace("@@", "")
