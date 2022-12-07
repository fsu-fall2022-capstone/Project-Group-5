import xml.etree.ElementTree as ET
from datetime import datetime

import discord

from nationstates_bot import NationStatesBot
from ns_bot.formatting import Formatter

class FormatWAInfo(Formatter):
    @classmethod
    async def format(
        cls,
        council,
        shard: str,
        data: str,
        bot: NationStatesBot,
        interaction: discord.Interaction
    ) -> None:

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text
        if not shard:
            await interaction.response.send_message(
                embed=discord.Embed(title=f"{council}")
            )