import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from aiohttp import ClientSession
from PIL import Image

from ns_bot.formatting import Formatter
from ns_bot.utils.wrappers import async_wrapper


class FormatRegionInfo(Formatter):
    async def __init__(self, interaction: discord.Interaction, shard: str, data: str) -> None:
        await interaction.response.send_message(
            embed=discord.Embed(title="Region Info", description=data)
        )
