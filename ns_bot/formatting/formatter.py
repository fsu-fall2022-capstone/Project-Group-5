import xml.etree.ElementTree as ET

from ns_bot.utils.wrappers import async_wrapper


class Formatter:
    BASE_BANNER_URL = "https://www.nationstates.net/images/banners/"
    BASE_REGION_URL = "https://www.nationstates.net//images/rbanners/uploads/"
    IMAGE_LIMIT = 10

    async_xml_parse = async_wrapper(ET.fromstring)

    @staticmethod
    def clean_data(data: str):
        if not data:
            return data
        return data.replace("&quot;", '"').replace("@@", "").replace("%%", "")
