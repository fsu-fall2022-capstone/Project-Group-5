import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from aiohttp import ClientSession
from PIL import Image

from ns_bot.utils.wrappers import async_wrapper


def format_region_info(data, shard):
    return discord.Embed(title="Region Info", description=data)
