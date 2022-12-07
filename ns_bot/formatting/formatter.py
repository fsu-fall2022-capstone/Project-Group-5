import xml.etree.ElementTree as ET
from io import BytesIO

from discord import Embed, File, Interaction

from ns_bot.DAOs.nationstates_api import NationStatesAPI
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

    @staticmethod
    async def send_embed_with_flag_image(
        nationstates_api: NationStatesAPI, interaction: Interaction, embed: Embed, url: str
    ):
        if not url.lower().endswith("svg"):
            embed.set_image(url=url)
            return await interaction.response.send_message(embed=embed)

        flag = await nationstates_api.get_image(url)
        flag_file = BytesIO()
        flag.save(flag_file, format="PNG")
        flag_file.seek(0)
        file = File(flag_file, filename="flag_image.png")
        embed.set_image(url="attachment://flag_image.png")
        await interaction.response.send_message(file=file, embed=embed)
