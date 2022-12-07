import random
import xml.etree.ElementTree as ET
from datetime import datetime

import discord

from ns_bot.formatting import Formatter


class FormatWAInfo(Formatter):
    @classmethod
    async def format(
        cls, council: str, shard: str, data: str, interaction: discord.Interaction
    ) -> None:

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text
        match shard:
            case "numnations":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The World Assembly has a whooping {text} member nations!"
                    )
                )
            case "numdelegates":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"There are currently {text} people serving as delegates to the World Assembly!"
                    )
                )
            case "delegates":
                delegates = " \n".join([member for member in random.sample(text.split(","), k=25)])
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Here are just a few of the dedicated, hard-working delegates of the {council}: ",
                        description=delegates,
                    )
                )
            case "members":
                members = " \n".join([member for member in random.sample(text.split(","), k=25)])
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Some of the fine nations who claim membership on the {council}: ",
                        description=members,
                    )
                )
            case "happenings":
                embed = discord.Embed(
                    title="New things are always happening at the World Assembly!"
                )
                for id in root[0].findall("EVENT"):
                    happenings_results = {}
                    # TODO format "%%...%%" like a nation title.
                    # TODO format "@@...@@" like a proper noun.
                    for element in id:
                        happenings_results[element.tag] = (
                            element.text.replace("@@", "").replace("%%", "").strip()
                        )
                    time_stamp = happenings_results.get("TIMESTAMP")
                    temp = float(time_stamp)
                    dt = datetime.fromtimestamp(temp)
                    date = dt.strftime("%b %d %Y")
                    time = dt.strftime("%H:%M:%S")
                    embed.add_field(
                        name=f"On {date} at {time}", value=happenings_results.get("TEXT")
                    )
                await interaction.response.send_message(embed=embed)
            case "proposals":
                embed = discord.Embed(
                    title=f"The {council} has recently discussed these proposals: "
                )
                await interaction.response.send_message(embed=embed)
            case "resolution":
                await interaction.response.send_message(embeds=cls.build_resolution_embeds(root))
            case "voters":
                embeds = cls.build_resolution_embeds(root)
                await interaction.response.send_message(embeds=embeds)
            case "votetrack":
                embeds = cls.build_resolution_embeds(root)
                await interaction.response.send_message(embeds=embeds)
            case "dellog":
                embeds = cls.build_resolution_embeds(root)
                embed_c = discord.Embed(title="The Delegate Log reads as follows:")
                i = 0
                for id in root[0].find("DELLOG").findall("ENTRY"):
                    if i < 26:
                        entries = {}
                        for element in id:
                            entries[element.tag] = element.text
                        time_stamp = entries.get("TIMESTAMP")
                        dt = datetime.fromtimestamp(float(time_stamp))
                        date = dt.strftime("%b %d %Y")
                        time = dt.strftime("%H:%M:%S")
                        embed_c.add_field(
                            name=f"On {date} at {time}:",
                            value=f"The nation of {entries.get('NATION')} voted {entries.get('ACTION')} with {entries.get('VOTES')} total votes.",
                            inline=False,
                        )
                        i += 1
                    else:
                        break
                embeds.append(embed_c)
                await interaction.response.send_message(embeds=embeds)
            case "delvotes":
                embeds = cls.build_resolution_embeds(root)
                await interaction.response.send_message(embeds=embeds)
            case "lastresolution":
                await interaction.response.send_message(embed=discord.Embed(title=f"{text}"))

    @classmethod
    def build_resolution_embeds(cls, root: ET.Element):
        description = root[0].find("DESC").text.replace("[list]", "").replace("[/list]", "").strip()
        description_embed = discord.Embed(
            title=f"{root[0].find('NAME').text}", description=description
        )

        author = root[0].find("PROPOSED_BY").text
        created = datetime.fromtimestamp(float(root[0].find("CREATED").text))
        created_date = created.strftime("%b %d %Y")
        created_time = created.strftime("%H:%M:%S")
        nations_yes = int(root[0].find("TOTAL_NATIONS_FOR").text)
        nations_no = int(root[0].find("TOTAL_NATIONS_AGAINST").text)
        votes_yes = int(root[0].find("TOTAL_VOTES_FOR").text)
        votes_no = int(root[0].find("TOTAL_VOTES_AGAINST").text)
        promoted = datetime.fromtimestamp(float(root[0].find("PROMOTED").text))
        prompted_date = promoted.strftime("%b %d %Y")
        prompted_time = promoted.strftime("%H:%M:%S")
        if votes_yes > votes_no:
            result = "is expected to pass"
        else:
            result = "is not expected to pass"
        stats_embed = discord.Embed(
            description=f"""This resolution was proposed by {author} on {created_date} at {created_time}.
            \nA total of {nations_yes + nations_no} nations have voted on this resolution.
            \nThere are currently {nations_yes} nations in favor of the resolution.
            \nThere are currently {nations_no} nations against the resolution.
            \n{votes_yes} delegates have voted in favor of passing the resolution.
            \n{votes_no} delegates have voted against the resolution.
            \nThe resolution {result}.
            \nThe resolution was promoted on {prompted_date} at {prompted_time}."""
        )
        return [description_embed, stats_embed]
