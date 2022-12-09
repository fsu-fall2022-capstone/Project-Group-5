import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from PIL import Image

from nationstates_bot import NationStatesBot
from ns_bot.formatting import Formatter


class FormatNationInfo(Formatter):
    @classmethod
    async def format(
        cls,
        nation: str,
        shard: str,
        data: str,
        bot: NationStatesBot,
        interaction: discord.Interaction,
    ) -> None:

        if not data:
            return await interaction.response.send_message(
                f"There was no response from Nation States with the nation {nation}",
                ephemeral=True,
            )

        data = cls.clean_data(data)
        root: ET.Element = await cls.async_xml_parse(data)
        text = root[0].text

        if not shard:
            if text is None:
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} has no dispatch list.")
                )
                return
            desc = ""
            flag_url: str = "https://www.nationstates.net/images/flags/Default.svg"
            for id in root:
                if id.tag == "FLAG":
                    flag_url = id.text
                elif id.tag == "FIRSTLOGIN" or id.tag == "LASTLOGIN":
                    time_stamp = datetime.fromtimestamp(float(id.text))
                    desc += f"\n{id.tag}: {time_stamp}\n"
                else:
                    desc += f"\n{id.tag}: {id.text}"
                for element in id:
                    if element.tag == "CAUSE":
                        desc += f"-{element.attrib}: {element.text.strip()}\n"
                    else:
                        desc += f"-{element.tag}: {element.text.strip()}\n"
            embed = discord.Embed(title=f"National information for {nation}", description=desc)
            embed.set_thumbnail(url=flag_url)
            await interaction.response.send_message(embed=embed)

        match shard:
            case "admirable":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The people of {nation} are well-known for being very {text}."
                    )
                )
            case "admirables":
                traits = ", ".join([trait.text for trait in root[0]])
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The people of {nation} are known to be {traits}.")
                )
            case "animal":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation}'s national animal is the {text.title()}")
                )
            case "animaltrait":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation}'s national animal {text}.")
                )
            case "answered":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} has voted on {text} issues")
                )
            case "banner":
                embed = discord.Embed(title=f"Banner of {nation}.")
                await cls.send_embed_with_flag_image(
                    bot.nationstates_api, interaction, embed, cls.BASE_BANNER_URL + text
                )
            case "banners":
                await cls.handle_banners(interaction, nation, root, bot)
            case "capital":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{text.title()} is the capital city of {nation} ")
                )
            case "category":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} is a {text}.")
                )
            case "census":
                embed = discord.Embed(title=f"{nation}'s standings")
                embed.add_field(name="World Ranking", value=root[0][0][1].text)
                embed.add_field(name="Rank within the Region", value=root[0][0][2].text)
                embed.add_field(name="Score", value=root[0][0][0].text)
                await cls.handle_census(root, embed, interaction)
            case "crime":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation}'s crime", description=text)
                )
            case "currency":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The {text} is the national currency of {nation}")
                )
            case "customleader":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation} has no custom leader."
                        if text is None
                        else f"{nation}'s leader is {text}"
                    )
                )
            case "customcapital":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation} has no custom capital."
                        if text is None
                        else f"{nation}'s capital is {text}"
                    )
                )
            case "customreligion":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation} has no custom religion."
                        if text is None
                        else f"{nation}'s custom religion is: {text}"
                    )
                )
            case "dbid":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The database ID for {nation} is {text}")
                )
            case "deaths":
                embed = discord.Embed(title=f"Causes of death in {nation}")
                for cause in root[0].iterfind("CAUSE"):
                    embed.add_field(
                        name=f"{cause.attrib['type']}",
                        value=f"{cause.text}%",
                        inline=False,
                    )
                await interaction.response.send_message(embed=embed)
            case "demonym":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"A citizen of {nation} is a {text}")
                )
            case "demonym2":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Another common name for a citizen of {nation} is {text}",
                    )
                )
            case "demonym2plural":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"A group of citizens from {nation} are called {text}"
                    )
                )
            case "dispatches":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} has had {text} dispatches")
                )
            case "dispatchlist":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no dispatch list.")
                    )
                    return
                embed = discord.Embed(title=f"Dispatch list for {nation}")
                for id in root[0].findall("DISPATCH")[:25]:
                    embed.add_field(
                        name=f"Dispatch ID: {id.attrib.get('id')}",
                        value="\n".join(f"{element.tag}: {element.text.strip()}" for element in id),
                    )
                await interaction.response.send_message(embed=embed)
            case "endorsements":
                if text:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{nation} has been endorsed by {len(root[0].findall('ENDORSEMENT'))} nations",
                        )
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has been endorsed by zero nations!")
                    )
            case "factbooks":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} has a written {text} factbooks.")
                )
            case "factbooklist":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no factbook list.")
                    )
                embed = discord.Embed(title=f"Fact book for {nation}")
                for id in root[0].findall("FACTBOOK")[:25]:
                    embed.add_field(
                        name=f"Fact book ID: {id.attrib.get('id')}",
                        value="\n".join(f"{element.tag}: {element.text.strip()}" for element in id),
                    )
                await interaction.response.send_message(embed=embed)
            case "firstlogin":
                temp = float(text)
                dt = datetime.fromtimestamp(temp)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The nation of {nation} was first logged in on {dt}."
                    )
                )
            case "flag":
                embed = discord.Embed(title=f"{nation}'s flag", url=text)
                await cls.send_embed_with_flag_image(bot.nationstates_api, interaction, embed, text)
            case "founded":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} was founded {text}!")
                )
            case "foundedtime":
                temp = float(text)
                dt = datetime.fromtimestamp(temp)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The nation of {nation} was founded at {dt}.")
                )
            case "freedom":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The nation of {nation} has a {root[0][0].text.lower()} record of civil rights, an economy considered by many to be {root[0][1].text.lower()}, and a political system that is {root[0][2].text.lower()}."
                    )
                )
            case "fullname":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The proper name of {nation} is `{text}`.")
                )
            case "gavote":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation}'s status in the General Assembly is currently {text}."
                    )
                )
            case "gdp":
                national_currency = bot.nation_dump.get(nation, {}).get("CURRENCY", "Dollars")
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} has a GDP of {text} {national_currency}!")
                )
            case "govt":
                embed = discord.Embed(title=f"{nation}'s government")
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation} Government split",
                        description=f"Administration:{root[0].findtext('ADMINISTRATION')}%\
                        \nDefence:{root[0].findtext('DEFENCE')}%\
                        \nEducation:{root[0].findtext('EDUCATION')}%\
                        \nEnvironment:{root[0].findtext('ENVIRONMENT')}%\
                        \nHealthcare:{root[0].findtext('HEALTHCARE')}%\
                        \nCommerce:{root[0].findtext('COMMERCE')}%\
                        \nInternational Aid:{root[0].findtext('INTERNATIONALAID')}%\
                        \nLaw and Order:{root[0].findtext('LAWANDORDER')}%\
                        \nPublic Transport:{root[0].findtext('PUBLICTRANSPORT')}%\
                        \nSocial Equality:{root[0].findtext('SOCIALEQUALITY')}%\
                        \nSpirituality:{root[0].findtext('SPIRITUALITY')}%\
                        \nWelfare:{root[0].findtext('WELFARE')}%\n",
                    )
                )
            case "govtdesc":
                await interaction.response.send_message(embed=discord.Embed(title=text))
            case "govtpriority":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The government of {nation} prioritizes their {text} above all else."
                    )
                )
            case "happenings":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no happenings.")
                    )
                    return
                embed = discord.Embed(title=f"Happenings for {nation}")
                for id in root[0].findall("EVENT"):
                    happenings_results = {}
                    for element in id:
                        happenings_results[element.tag] = element.text.strip()
                    time_stamp = happenings_results.get("TIMESTAMP")
                    temp = float(time_stamp)
                    dt = datetime.fromtimestamp(temp)
                    embed.add_field(name=dt, value=happenings_results.get("TEXT"))
                await interaction.response.send_message(embed=embed)
            case "income":
                national_currency = bot.nation_dump.get(nation, {}).get("CURRENCY", "Dollar")
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The average income for a resident of {nation} is {text} {national_currency}."
                    )
                )
            case "industrydesc":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Industry description for {nation}", description=text
                    )
                )
            case "influence":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The nation of {nation} spreads its influence by being a {text}."
                    )
                )
            case "lastactivity":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} had their most recent activity {text}.")
                )
            case "lastlogin":
                temp = float(text)
                dt = datetime.fromtimestamp(temp)
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} was last logged in {dt}.")
                )
            case "leader":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{text} is the current leader of {nation}.")
                )
            case "legislation":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no dispatch list.")
                    )
                    return
                embed = discord.Embed(title=f"Legislation for {nation}")
                for counter, id in enumerate(root[0].findall("LAW")):
                    embed.add_field(
                        name="\u200b", value=f"{counter + 1}) {id.text}. ", inline=False
                    )
                await interaction.response.send_message(embed=embed)
            case "majorindustry":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{text} is the biggest industry of {nation}!")
                )
            case "motto":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f'"{text}"' + f" is the motto of {nation}.")
                )
            case "name":
                await interaction.response.send_message(embed=discord.Embed(title=text))
            case "notable":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} is known for their {text}.")
                )
            case "notables":
                notables = "\n".join([notables.text for notables in root[0]])
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The people of {nation} are known for:\n", description=notables
                    )
                )
            case "policies":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no policies")
                    )
                    return
                embed = discord.Embed(title=f"Policies for {nation}")
                for id in root[0].findall("POLICY")[:25]:
                    embed.add_field(
                        name="\u200b",
                        value="\n".join(f"{element.tag}: {element.text.strip()}" for element in id),
                    )
                await interaction.response.send_message(embed=embed)
            case "poorest":
                national_currency = bot.nation_dump.get(nation, {}).get("CURRENCY", "Dollar")
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The poorest people in {nation}, on average have a reported income of {text} {national_currency}."
                    )
                )
            case "population":
                if len(text) < 4:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has a population of {text} million")
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{nation} has a population of {round(float(text) / 1000, 2)} billion."
                        )
                    )
            case "publicsector":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{text}% of {nation}'s economy is from the publicsector."
                    )
                )
            case "rcensus":
                embed = discord.Embed(title=f"{nation}'s Region standing.")
                embed.add_field(name="Rank", value=text)
                await cls.handle_census(root, embed, interaction)
            case "region":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} can be found in the {text} region.")
                )
            case "religion":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{text} is the official religion of {nation}.")
                )
            case "richest":
                national_currency = bot.nation_dump.get(nation, {}).get("CURRENCY", "Dollars")
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"The richest people in {nation}, on average have a reported income of {text} {national_currency}."
                    )
                )
            case "scvote":
                if text:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{nation}'s status on the Security Council is currently {text}."
                        )
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{nation} is not a member of the Security Council."
                        )
                    )
            case "sectors":
                if text is None:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no sector information.")
                    )
                    return
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation} sectors split",
                        description=f"Blackmarket: {root[0].findtext('BLACKMARKET')}%\
                        \nGovernment: {root[0].findtext('GOVERNMENT')}%\
                        \nIndustry: {root[0].findtext('INDUSTRY')}%\
                        \nPublic: {root[0].findtext('PUBLIC')}%\n",
                    )
                )
            case "sensibilities":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The people of {nation} are known to be {text}.")
                )
            case "tax":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"The average tax rate in {nation} is {text}%.")
                )
            case "tgcanrecruit":
                if text == "1":
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} can receive recruitment telegrams.")
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            title=f"{nation} can not receive recruitment telegrams."
                        )
                    )
            case "tgcancampaign":
                if text == "1":
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} can receive campaign telegrams.")
                    )
                else:
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} can not receive campaign telegrams.")
                    )
            case "type":
                await interaction.response.send_message(
                    embed=discord.Embed(title=f"{nation} is a {text}!")
                )
            case "wa":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"{nation}'s membership status in the World Assembly is: {text}."
                    )
                )
            case "wabadges":
                badges = ",".join([badges.text for badges in root[0]])
                if badges == "":
                    await interaction.response.send_message(
                        embed=discord.Embed(title=f"{nation} has no world assembly badges.")
                    )
                    return
                embed = discord.Embed(
                    title=f"{nation} has been commended by the following Security Council Resolutions:",
                    description=badges,
                )
                await interaction.response.send_message(embed=embed)
            case "wcensus":
                embed = discord.Embed(title=f"{nation}'s World standing.")
                embed.add_field(name="Rank", value=text)
                await cls.handle_census(root, embed, interaction)
            case "zombie":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title=f"Zombie information for {nation}",
                        description=f"Z ACTION: {root[0].findtext('ZACTION')}\
                        \nZ Action Intended: {root[0].findtext('ZACTIONINTENDED')}\
                        \nIndustry: {root[0].findtext('SURVIVORS')}\
                        \nZombies: {root[0].findtext('ZOMBIES')}\
                        \nDead: {root[0].findtext('DEAD')}\n",
                    )
                )

    @staticmethod
    async def handle_census(
        root: ET.Element, embed: discord.Embed, interaction: discord.Interaction
    ):
        id = root[0][0].attrib.get("id")
        rank_image = Image.open(f"ns_bot/data/ranks/{id}.png")
        image_file = BytesIO()
        rank_image.save(image_file, format="PNG")
        image_file.seek(0)
        embed.set_thumbnail(url="attachment://rank.png")
        file = discord.File(image_file, filename="rank.png")
        await interaction.response.send_message(embed=embed, file=file)

    @classmethod
    async def handle_banners(
        cls, interaction: discord.Interaction, nation: str, root: ET.Element, bot: NationStatesBot
    ):
        await interaction.response.defer(thinking=True)

        banner_urls = [f"banners/{banner.text}" for banner in root[0]][: cls.IMAGE_LIMIT]
        image_results: list[Image.Image] = await bot.nationstates_api.get_banners(banner_urls)

        list_length = len(image_results)
        w = image_results[0].width
        h = image_results[0].height
        half_len = -(-list_length // 2)

        compiled_banners_image = Image.new(
            mode="RGB", size=(w * 2, h * (half_len)), color=(47, 49, 54)
        )

        for i, banner in enumerate(image_results):
            # left column
            if i < list_length:
                compiled_banners_image.paste(banner, (0, h * i))
            # right column
            compiled_banners_image.paste(banner, (w, h * (i - half_len)))

        image_file = BytesIO()
        compiled_banners_image.save(image_file, format="PNG")
        image_file.seek(0)
        image_file = discord.File(image_file, filename="banner_images.png")

        embed = discord.Embed(title=f"Banners for {nation}.")
        embed.set_image(url="attachment://banner_images.png")
        await interaction.followup.send(embed=embed, file=image_file)
