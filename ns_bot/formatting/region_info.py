import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from aiohttp import ClientSession
from PIL import Image

from ns_bot.formatting import Formatter
from ns_bot.utils.wrappers import async_wrapper


class FormatRegionInfo(Formatter):
    @classmethod
    async def format(
        cls,
        region: str,
        interaction: discord.Interaction,
        shard: str,
        data: str,
    ) -> None:

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text

        if not shard:
            if text is None:
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region} has no dispatch list.")
                )
        match shard:
            case "banner":
                embed = discord.Embed(title=f"Banner of {region}.")
                embed.set_image(url=f"{cls.BASE_REGION_URL}{region}__{text}.jpg")
                print(f"{cls.BASE_REGION_URL}{region}__{text}.jpg")
                await interaction.response.send_message(embed=embed)
            case "bannerby":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region}'s region banner was created by:  {text}")
                )
            case "bannerurl":
                pass
            case "census":
                pass
            case "censusranks":
                pass
            case "dbid":
                pass
            case "delegate":
                pass
            case "delegateauth":
                pass
            case "delegatevotes":
                pass
            case "dispatches":
                pass
            case "embassies":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"There are no embassies in {region}")
                    )
                embed = discord.Embed(title=f"Embassies in {region}")
                for embassy in root[0].iterfind("EMBASSY"):
                    embed.add_field(
                        name=f"{embassy.attrib['type']}:",
                        value=f"{embassy.text}",
                        inline=False,
                    )
                await interaction.response.send_message(embed=embed)
            case "embassyrmb":
                pass
            case "factbook":
                pass
            case "flag":
                pass
            case "founded":
                pass
            case "foundedtime":
                pass
            case "founder":
                pass
            case "founderauth":
                pass
            case "gavote":
                pass
            case "happenings":
                pass
            case "history":
                pass
            case "lastupdate":
                pass
            case "messages":
                pass
            case "name":
                pass
            case "nations":
                pass
            case "numnations":
                pass
            case "officers":
                pass
            case "poll":
                pass
            case "power":
                pass
            case "scvote":
                pass
            case "tags":
                pass
            case "wabadges":
                pass
            case "zombie":
                pass

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Region Info",
                description=data,
            )
        )
