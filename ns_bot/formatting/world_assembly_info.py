import xml.etree.ElementTree as ET
from datetime import datetime

import discord
import random

from nationstates_bot import NationStatesBot
from ns_bot.formatting import Formatter

class FormatWAInfo(Formatter):
    @classmethod
    async def format(
        cls,
        council,
        shard: str,
        data: str,
        interaction: discord.Interaction
    ) -> None:

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text
        match shard:
            case "numnations":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The {council} has a whooping {text} member nations!")
                )
            case "numdelegates":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"There are currently {text} people serving as delegates to the {council}!")
                )
            case "delegates":
                delegates = " \n".join([member for member in random.sample(text.split(','), k=25)])
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Here are just a few of the dedicated, hard-working delegates of the {council}: ", description=delegates)
                )
            case "members":
                members = " \n".join([member for member in random.sample(text.split(','), k=25)])
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Some of the fine nations who claim membership on the {council}: ", description=members)
                )
            case "happenings":
                embed = discord.Embed(title=f"New things are always happening at the World Assembly!")
                for id in root[0].findall("EVENT"):
                    happenings_results = {}
                    # TODO format "%%...%%" like a nation title.
                    # TODO format "@@...@@" like a proper noun.
                    for element in id:
                        happenings_results[element.tag] = element.text.replace("@@","").replace("%%","").strip()
                    time_stamp = happenings_results.get("TIMESTAMP")
                    temp = float(time_stamp)
                    dt = datetime.fromtimestamp(temp)
                    date = dt.strftime("%b %d %Y")
                    time = dt.strftime("%H:%M:%S")
                    embed.add_field(name=f"On {date} at {time}", value=happenings_results.get("TEXT"))
                await interaction.response.send_message(embed=embed)