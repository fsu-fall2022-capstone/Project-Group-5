import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from aiohttp import ClientSession
from PIL import Image

from ns_bot.formatting import Formatter
from ns_bot.utils.wrappers import async_wrapper

# test push
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
                    embed=discord.Embed(title=f"{region}'s region banner was created by: {text}")
                )
            case "bannerurl":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Banner URL", description=text, url=cls.BASE_REGION_URL + text
                    )
                )
            case "census":
                embed = discord.Embed(title=f"{region}'s __ standing")
                embed.add_field(name="World Ranking", value=root[0][0][1].text, inline=False)
                embed.add_field(name="Score", value=root[0][0][0].text, inline=False)
                await interaction.response.send_message(embed=embed)
            case "censusranks":
                pass
            case "dbid":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The database ID for {region} is {text}")
                )
            case "delegate":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate {text}")
                )
            case "delegateauth":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate Auth {text}")
                )
            case "delegatevotes":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate Votes {text}")
                )
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
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The flag of {region}", url=text)
                )
            case "founded":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region} founded {text}")
                )
            case "foundedtime":
                temp = float(text)
                dt = datetime.fromtimestamp(temp)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The region of {region} was founded at {dt}.")
                )
            case "founder":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Founder of {region}: {text}")
                )
            case "founderauth":
                pass
            case "gavote":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{region}'s status in the General Assembly is currently {text}."
                    )
                )
            case "happenings":
                pass
            case "history":
                pass
            case "lastupdate":
                temp = float(text)
                dt = datetime.fromtimestamp(temp)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The region of {region} was last updated at {dt}.")
                )
            case "messages":
                pass
            case "name":
                await interaction.response.send_message(embed=discord.Embed(title=text))
            case "nations":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Nations in {region}: {text}")
                )
            case "numnations":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Number of nations in {region}: {text}")
                )
            case "officers":
                pass
            case "poll":
                pass
            case "power":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region}'s power is {text}")
                )
            case "scvote":
                if text:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{region}'s status on the Security Council is currently {text}."
                        )
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{region} is not a member of the Security Council."
                        )
                    )
            case "tags":
                pass
            case "wabadges":
                pass
            case "zombie":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Zombie information for {region}",
                        description=f"Industry: {root[0].findtext('SURVIVORS')}\
                        \nZombies: {root[0].findtext('ZOMBIES')}\
                        \nDead: {root[0].findtext('DEAD')}\n",
                    )
                )

        await interaction.response.send_message(
            embed=discord.Embed(
                title="Region Info",
                description=data,
            )
        )
