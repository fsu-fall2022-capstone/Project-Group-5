import re
import xml.etree.ElementTree as ET
from datetime import datetime

import discord

from nationstates_bot import NationStatesBot
from ns_bot.formatting import Formatter


class FormatRegionInfo(Formatter):
    @classmethod
    async def format(
        cls,
        region: str,
        shard: str,
        data: str,
        interaction: discord.Interaction,
        bot: NationStatesBot,
    ) -> None:

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text

        if not data:
            return await interaction.response.send_message(
                f"{region} is unknown. Please try again", ephemeral=True
            )

        if not shard:
            if text is None:
                return await interaction.response.send_message(
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
                banner_url = cls.BASE_REGION_URL + text.split("/")[-1]
                embed = discord.Embed(title="Banner URL", description=text, url=banner_url)
                await cls.send_embed_with_flag_image(
                    bot.nationstates_api, interaction, embed, banner_url
                )
            case "census":
                embed = discord.Embed(title=f"{region}'s __ standing")
                embed.add_field(name="World Ranking", value=root[0][0][1].text, inline=False)
                embed.add_field(name="Score", value=root[0][0][0].text, inline=False)
                await interaction.response.send_message(embed=embed)
            case "censusranks":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no census ranks.")
                    )
                    return
                embed = discord.Embed(title=f"Census ranks in {region}")
                for id in root[0].findall("NATIONS")[:25]:
                    for element in id:
                        embed.add_field(
                            name="\u200b",
                            value="\n".join(
                                f"{element_text.tag}: {element_text.text.strip()}"
                                for element_text in element
                            ),
                        )
                await interaction.response.send_message(embed=embed)
            case "dbid":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The database ID for {region} is {text}")
                )
            case "delegate":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate {text}")
                )
            case "delegateauth":
                embed = discord.Embed(title="Delegate Auth:")
                for id in text:
                    if id == "X":
                        embed.add_field(name="\u200b", value="Execute", inline=False)
                    elif id == "W":
                        embed.add_field(name="\u200b", value="World Assembly", inline=False)
                    elif id == "A":
                        embed.add_field(name="\u200b", value="Appearance", inline=False)
                    elif id == "B":
                        embed.add_field(name="\u200b", value="Border Control", inline=False)
                    elif id == "C":
                        embed.add_field(name="\u200b", value="Communications", inline=False)
                    elif id == "E":
                        embed.add_field(name="\u200b", value="Embassies", inline=False)
                    elif id == "P":
                        embed.add_field(name="\u200b", value="Polls", inline=False)
                await interaction.response.send_message(embed=embed)
            case "delegatevotes":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate Votes {text}")
                )
            case "dispatches":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no dispatches.")
                    )
                    return
                embed = discord.Embed(
                    title=f"Dispatches in {region}", description=text.replace(",", "\n")
                )
                await interaction.response.send_message(embed=embed)
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
                if text == "0":
                    embassy_response = "no-one"
                elif text == "con":
                    embassy_response = "delegates & Founders of embassy regions"
                elif text == "off":
                    embassy_response = "officers of embassy regions"
                elif text == "com":
                    embassy_response = "officers of embassy regions with Communications authority"
                elif text == "all":
                    embassy_response = "all residents of embassy regions"
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Embassy posting privileges are extended to {embassy_response}"
                    )
                )
            case "factbook":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"There is no factbook in {region}")
                    )
                # replace text between brackets to clean up special characters
                output = re.sub(r"\[.*?\]", " ", text)
                embed = discord.Embed(title=f"Factbook in {region}", description=output)
                await interaction.response.send_message(embed=embed)
            case "flag":
                embed = discord.Embed(title=f"{region}'s flag", url=text)
                await cls.send_embed_with_flag_image(bot.nationstates_api, interaction, embed, text)
            case "founded":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region} founded {text}")
                )
            case "foundedtime":
                time = float(text)
                dt = datetime.fromtimestamp(time)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The region of {region} was founded at {dt}.")
                )
            case "founder":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{region} founded by {text}")
                )
            case "founderauth":
                text = cls.authority_code_to_string(text)
                embed = discord.Embed(title="Founder Auth:", description=text)
                await interaction.response.send_message(embed=embed)
            case "gavote":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{region}'s status in the General Assembly is currently {text}."
                    )
                )
            case "happenings":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no happenings in their region.")
                    )
                embed = discord.Embed(title=f"Happenings for the region {region}")
                for id in root[0].findall("EVENT"):
                    happenings_results = {}
                    for element in id:
                        happenings_results[element.tag] = element.text.strip()
                    time_stamp = happenings_results.get("TIMESTAMP")
                    time = float(time_stamp)
                    dt = datetime.fromtimestamp(time)
                    embed.add_field(name=dt, value=happenings_results.get("TEXT"))
                await interaction.response.send_message(embed=embed)
            case "history":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no history.")
                    )
                    return
                embed = discord.Embed(title=f"History of {region}")
                for id in root[0].findall("EVENT"):
                    history_results = {}
                    for element in id:
                        history_results[element.tag] = element.text.strip()
                    time_stamp = history_results.get("TIMESTAMP")
                    time = float(time_stamp)
                    dt = datetime.fromtimestamp(time)
                    embed.add_field(name=dt, value=history_results.get("TEXT"))
                await interaction.response.send_message(embed=embed)
            case "lastupdate":
                time = float(text)
                dt = datetime.fromtimestamp(time)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The region of {region} was last updated at {dt}.")
                )
            case "messages":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no messages")
                    )
                    return
                embed = discord.Embed(title=f"Messages in {region}")
                for id in root[0].findall("POST")[:25]:
                    embed.add_field(
                        name="\u200b",
                        value="\n".join(f"{element.tag}: {element.text.strip()}" for element in id),
                    )
                await interaction.response.send_message(embed=embed)
            case "name":
                await interaction.response.send_message(embed=discord.Embed(title=text))
            case "nations":
                # TODO fix. title will end up way too long.
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Nations in {region}: {text}")
                )
            case "numnations":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Number of nations in {region}: {text}")
                )
            case "officers":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{region} has no officers")
                    )
                    return
                embed = discord.Embed(title=f"Officers in {region}")
                for officer in root[0].findall("OFFICER")[:25]:
                    nation_name = officer.findtext("NATION")
                    office = officer.findtext("OFFICE")
                    authority = officer.findtext("AUTHORITY")
                    authority = cls.authority_code_to_string(authority)
                    time = cls.timestamp_to_datetime_str(officer.findtext("TIME"))
                    by = officer.findtext("BY")
                    order = officer.findtext("ORDER")
                    embed.add_field(
                        name=nation_name,
                        value=f"Office: {office}\
                            \nWas added {time}\
                            \nBy {by}\
                            \nAt position {order}\
                            \nHolding the authority of :\n{authority}",
                    )
                await interaction.response.send_message(embed=embed)
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
                embed = discord.Embed(title=f"Tags for {region}")
                root[0].find("TAGS")
                tags_results = {}
                for element in root[0]:
                    embed.add_field(name="\u200b", value=element.text.strip(), inline=False)
                await interaction.response.send_message(embed=embed)
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

    @staticmethod
    def authority_code_to_string(codes: str):
        codes = codes.replace("E", "Embassies\n")
        codes = codes.replace("A", "Appearance\n")
        codes = codes.replace("C", "Communications\n")
        codes = codes.replace("P", "Poll\n")
        codes = codes.replace("X", "Execute\n")
        codes = codes.replace("B", "Border Control\n")
        codes = codes.replace("W", "World Assembly\n")
        return codes
