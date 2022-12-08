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
                # TODO Convert text to:
                """
                X: Executive
                W: World Assembly
                A: Appearance
                B: Border Control
                C: Communications
                E: Embassies
                P: Polls
                """
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"Delegate Auth {text}")
                )
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
                pass
            case "factbook":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"There is no factbook in {region}")
                    )
                # replace text between brackets to clean up special characters
                output = re.sub("\[.*?\]", " ", text)
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
                    temp = float(time_stamp)
                    dt = datetime.fromtimestamp(temp)
                    embed.add_field(name=dt, value=happenings_results.get("TEXT"))
                await interaction.response.send_message(embed=embed)
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
                # TODO fix. title will end up way too long.
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
