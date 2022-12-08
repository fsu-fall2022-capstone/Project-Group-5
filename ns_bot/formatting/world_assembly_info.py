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

        if not data:
            return await interaction.response.send_message(
                "There was no response from Nation States", ephemeral=True
            )

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
                for event in root[0].findall("EVENT"):
                    happening = (
                        event.findtext("TEXT").replace("@@", "**").replace("%%", "*").strip()
                    )
                    date_time = cls.timestamp_to_datetime_str(event.findtext("TIMESTAMP"))
                    embed.add_field(name=f"{date_time}", value=happening)
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
                nations_for = "\n".join([ nation.text for nation in random.sample(root[0].find("VOTES_FOR").findall('N'), k=25)])
                nations_for_embed = discord.Embed(
                    title="A random selection of nations who voted FOR the resolution:",
                    description=nations_for
                )
                embeds.append(nations_for_embed)
                nations_against = "\n".join([ nation.text for nation in random.sample(root[0].find("VOTES_AGAINST").findall('N'), k=25)])
                nations_against_embed = discord.Embed(
                    title="A random selection of nations who voted AGAINST the resolution:",
                    description=nations_against
                )
                embeds.append(nations_against_embed)
                await interaction.response.send_message(embeds=embeds)
            case "votetrack":
                embeds = cls.build_resolution_embeds(root)
                await interaction.response.send_message(embeds=embeds)
            case "dellog":
                embeds = cls.build_resolution_embeds(root)
                dellog_embed = discord.Embed(
                    title="A random part of The Delegate Log reads as follows:"
                )
                entries = random.sample(root[0].find("DELLOG").findall("ENTRY"), k=25)
                for entry in entries:
                    date_time = cls.timestamp_to_datetime_str(entry.find('TIMESTAMP').text)
                    dellog_embed.add_field(
                        name=f"{date_time}",
                        value=f"The nation of {entry.find('NATION').text} voted {entry.find('ACTION').text} with {entry.find('VOTES').text} total votes.",
                    )
                embeds.append(dellog_embed)
                await interaction.response.send_message(embeds=embeds)
            case "delvotes":
                embeds = cls.build_resolution_embeds(root)
                delvotes_for_embed = discord.Embed(
                    title="A random selection of delegates FOR the resolution:"
                )
                votes_against = random.sample(root[0].find("DELVOTES_FOR").findall("DELEGATE"), k=25)
                for vote in votes_against:
                    date_time = cls.timestamp_to_datetime_str(vote.find('TIMESTAMP').text)
                    delvotes_for_embed.add_field(
                        name=f"{date_time}",
                        value=f"{vote.find('NATION').text} cast {vote.find('VOTES').text} votes."
                    )
                embeds.append(delvotes_for_embed)
                delvotes_against_embed = discord.Embed(
                    title="A random selection of delegates AGAINST the resolution:"
                )
                votes_for = random.sample(root[0].find("DELVOTES_AGAINST").findall("DELEGATE"), k=25)
                for vote in votes_for:
                    date_time = cls.timestamp_to_datetime_str(vote.find('TIMESTAMP').text)
                    delvotes_against_embed.add_field(
                        name=f"{date_time}",
                        value=f"{vote.find('NATION').text} cast {vote.find('VOTES').text} votes."
                    )
                embeds.append(delvotes_against_embed)
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
