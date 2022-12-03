import xml.etree.ElementTree as ET
from datetime import datetime
from io import BytesIO

import discord
from aiohttp import ClientSession
from PIL import Image

from nationstates_bot import NationStatesBot
from ns_bot.utils.wrappers import async_wrapper

BASE_BANNER_URL = "https://www.nationstates.net/images/banners/"
IMAGE_LIMIT = 10


async def format_nation_info(
    nation: str, shard: str, data: str, bot: NationStatesBot, interaction: discord.Interaction
):
    web_session = bot.web_client
    async_parse = async_wrapper(ET.fromstring)
    root: ET.Element = await async_parse(data.replace("&quot;", '"'))
    text = root[0].text
    national_currency = bot.nation_dump.get(nation, {}).get("CURRENCY", "Dollars")
    if not shard:
        return [discord.Embed(title="Nation Info", description=data)]
    match shard:
        case "admirable":
            return [
                discord.Embed(title=f"The people of {nation} are well-known for being very {text}.")
            ]
        case "admirables":
            traits = ""
            for i in range(0, len(root[0])):
                if i == 0:
                    traits = traits + root[0][i].text
                elif i == len(root[0]) - 1:
                    traits = traits + ", and " + root[0][i].text
                else:
                    traits = traits + ", " + root[0][i].text
            return [discord.Embed(title=f"The people of {nation} are known to be {traits}.")]
        case "animal":
            return [discord.Embed(title=f"{nation}'s national animal is the: {text.title()}")]
        case "animaltrait":
            return [discord.Embed(title=f"The national animal of {nation} {text}.")]
        case "answered":
            return [discord.Embed(title=f"{nation} has voted on {text} issues")]
        case "banner":
            embed = discord.Embed(title=f"Banner of {nation}.")
            embed.set_image(url=BASE_BANNER_URL + text)
            return [embed]
        case "banners":
            await interaction.response.defer(thinking=True)
            banner_urls = [BASE_BANNER_URL + banner.text for banner in root[0]]
            list_length = len(banner_urls)
            if list_length > IMAGE_LIMIT:
                list_length = IMAGE_LIMIT

            results = []
            for url in banner_urls:
                async with web_session.get(
                    url, headers={"User-Agent": "NS Discord Bot"}
                ) as response:
                    results.append(Image.open(BytesIO(await response.content.read())))

            w = results[0].width
            h = results[0].height
            half_len = -(-list_length // 2)

            img = Image.new(mode="RGB", size=(w * 2, h * (half_len)), color=(47, 49, 54))

            for i in range(list_length):
                # left column
                if i < list_length:
                    img.paste(results[i], (0, h * i))
                # right column
                img.paste(results[i], (w, h * (i - half_len)))

            img_file = BytesIO()
            img.save(img_file, format="PNG")
            img_file.seek(0)
            img_file = discord.File(img_file, filename="image.png")
            embed = discord.Embed(title=f"Banners for {nation}.")
            embed.set_image(url="attachment://image.png")
            return [await interaction.followup.send(embed=embed, file=img_file)]
        case "capital":
            return [discord.Embed(title=f"{text.title()} is the capital city of {nation} ")]
        case "category":
            return [discord.Embed(title=f"{nation} is a {text}!")]
        case "census":
            embed = discord.Embed(title=f"{nation}'s Public Education standing")
            embed.add_field(name="World Ranking", value=root[0][0][1].text, inline=False)
            embed.add_field(name="Rank within the Region", value=root[0][0][2].text, inline=False)
            embed.add_field(name="Score on the ", value=root[0][0][0].text, inline=False)
            return [embed]
        case "crime":
            return [discord.Embed(title=f"{text.capitalize()}")]
        case "currency":
            return [
                discord.Embed(
                    title=f"The {text.capitalize()} is the national currency of {nation}",
                )
            ]
        case "customleader":
            if text is None:
                return [discord.Embed(title=f"{nation} has no custom leader.")]
            return [discord.Embed(title=f"{nation}'s custom leader is: {text}")]
        case "customcapital":
            if text is None:
                return [discord.Embed(title=f"{nation} has no custom capital.")]
            return [discord.Embed(title=f"{nation}'s custom capital is: {text}")]
        case "customreligion":
            if text is None:
                return [discord.Embed(title=f"{nation} has no custom religion.")]
            return [discord.Embed(title=f"{nation}'s custom religion is: {text}")]
        case "dbid":
            return [discord.Embed(title=f"Database ID for {nation}: {text}")]
        case "deaths":
            embed = discord.Embed(title=f"Causes of death in {nation}")
            for cause in root[0].iterfind("CAUSE"):
                embed.add_field(
                    name=f"{cause.text}% of people die from:",
                    value=f"{cause.attrib['type']}",
                    inline=False,
                )
            return [embed]
        case "demonym":
            return [discord.Embed(title=f"A person from {nation} is a {text}")]
        case "demonym2":
            return [
                discord.Embed(
                    title=f"Another common name for a person from {nation} is {text}",
                )
            ]
        case "demonym2plural":
            return [discord.Embed(title=f"A group of people from {nation} are called {text}")]
        case "dispatches":
            return [discord.Embed(title=f"{nation} has had {text} dispatches")]
        case "dispatchlist":
            if text is None:
                return [discord.Embed(title=f"{nation} has no dispatch list.")]
            embed = discord.Embed(title=f"Dispatch list for {nation}")
            results = {}
            for id in root[0].findall("DISPATCH"):
                for elem in id:
                    results[elem.tag] = elem.text.strip()
                    kvpair = ""
                    for k, v in results.items():
                        kvpair = kvpair + k + ": " + v + "\n"
                embed.add_field(name=f"Dispatch ID: {id.attrib.get('id')}", value=kvpair)
                results = {}
            return [embed]
        case "endorsements":
            if text:
                return [
                    discord.Embed(
                        title=f"{nation} has been endorsed by {len(root[0].findall('ENDORSEMENT'))} nations",
                    )
                ]
            else:
                return [discord.Embed(title=f"{nation} has been endorsed by zero nations!")]
        case "factbooks":
            return [
                discord.Embed(title=f"{nation} has a total of {text} factbooks written about them.")
            ]
        case "factbooklist":
            if text is None:
                return [discord.Embed(title=f"{nation} has no factbook list.")]
            return [discord.Embed(title="ERROR", description=data)]
        case "firstlogin":
            return [discord.Embed(title=f"The nation of {nation} was first logged in on {text}.")]
        case "flag":
            embed = discord.Embed(title=f"The flag of {nation}", url=text)
            return [embed]
        case "founded":
            return [discord.Embed(title=f"{nation} was founded exactly {text}!")]
        case "foundedtime":
            return [discord.Embed(title=f"The nation of {nation} was founded at {text}.")]
        case "freedom":
            sentence = f"The nation of {nation} has a {root[0][0].text.lower()} record of civil rights, an economy considered by many to be {root[0][1].text.lower()}, and a political system that is {root[0][2].text.lower()}."
            return [discord.Embed(title=sentence)]
        case "fullname":
            return [discord.Embed(title=f"The proper name of {nation} is '{text}'.")]
        case "gavote":
            return [
                discord.Embed(
                    title=f"{nation}'s status in the General Assembly is currently {text}."
                )
            ]
        case "gdp":
            return [discord.Embed(title=f"{nation} has a GDP of {text} {national_currency}!")]
        case "govt":
            pass
        case "govtdesc":
            return [discord.Embed(title=text)]
        case "govtpriority":
            return [
                discord.Embed(
                    title=f"The government of {nation} prioritizes their {text} above all else."
                )
            ]
        case "happenings":
            if text is None:
                return [discord.Embed(title=f"{nation} has no happenings.")]
            embed = discord.Embed(title=f"Happenings for {nation}")
            for id in root[0].findall("EVENT"):
                results = {}
                for elem in id:
                    results[elem.tag] = elem.text.strip()
                ts = results.get("TIMESTAMP")
                temp = float(ts)
                dt = datetime.fromtimestamp(temp)
                embed.add_field(name=dt, value=results.get("TEXT"))
            return [embed]
        case "income":
            return [
                discord.Embed(
                    title=f"The average income for a resident of {nation} is {text} {national_currency}."
                )
            ]
        case "industrydesc":
            return [discord.Embed(title=text)]
        case "influence":
            return [
                discord.Embed(
                    title=f"The nation of {nation} spreads its influence by being a {text}."
                )
            ]
        case "lastactivity":
            return [discord.Embed(title=f"{nation} had their most recent activity {text}.")]
        case "lastlogin":
            return [discord.Embed(title=f"{nation} was last logged in {text}.")]
        case "leader":
            return [discord.Embed(title=f"{text} is the current leader of {nation}.")]
        case "legislation":
            if text is None:
                return [discord.Embed(title=f"{nation} has no dispatch list.")]
            embed = discord.Embed(title=f"Dispatch list for {nation}")
            counter = 1
            for id in root[0].findall("LAW"):
                embed.add_field(name="\u200b", value=f"{counter}) {id.text}. ", inline=False)
                counter += 1
            return [embed]
        case "majorindustry":
            return [discord.Embed(title=f"{text} is the biggest industry of {nation}!")]
        case "motto":
            return [discord.Embed(title=f'"{text}"' + f" is the motto of {nation}.")]
        case "name":
            return [discord.Embed(title=nation)]
        case "notable":
            return [discord.Embed(title=f"{nation} is known for their {text}.")]
        case "notables":
            return [discord.Embed(title="ERROR", description=data)]
        case "policies":
            return [discord.Embed(title="ERROR", description=data)]
        case "poorest":
            return [
                discord.Embed(
                    title=f"The poorest people in {nation}, on average have a reported income of {text} {national_currency}."
                )
            ]
        case "population":
            if len(text) < 4:
                return [discord.Embed(title=f"{nation} has a population of {text} million")]
            else:
                return [
                    discord.Embed(
                        title=f"{nation} has a population of {float(text) / 1000} billion."
                    )
                ]
        case "publicsector":
            return [
                discord.Embed(
                    title=f"{text}% of {nation}'s economy is controlled by it's government."
                )
            ]
        case "rcensus":
            return [
                discord.Embed(
                    title=f"{nation}'s mining industry is ranked {text} within its region."
                )
            ]
        case "region":
            return [discord.Embed(title=f"{nation} can be found in the {text} region.")]
        case "religion":
            return [discord.Embed(title=f"{text} is the official religion of {nation}.")]
        case "richest":
            return [
                discord.Embed(
                    title=f"The richest people in {nation}, on average have a reported income of {text} {national_currency}."
                )
            ]
        case "scvote":
            if text:
                return [
                    discord.Embed(
                        title=f"{nation}'s status on the Security Council is currently {text}."
                    )
                ]
            else:
                return [discord.Embed(title=f"{nation} is not a member of the Security Council.")]
        case "sectors":
            pass
        case "sensibilities":
            return [discord.Embed(title=f"The people of {nation} are known to be {text}.")]
        case "tax":
            return [discord.Embed(title=f"The average tax rate in {nation} is {text}%.")]
        case "tgcanrecruit":
            if text == "1":
                return [discord.Embed(title=f"{nation} can receive recruitment telegrams.")]
            else:
                return [discord.Embed(title=f"{nation} can not receive recruitment telegrams.")]
        case "tgcancampaign":
            if text == "1":
                return [discord.Embed(title=f"{nation} can receive campaign telegrams.")]
            else:
                return [discord.Embed(title=f"{nation} can not receive campaign telegrams.")]
        case "type":
            return [discord.Embed(title=f"{nation} is a {text}!")]
        case "wa":
            return [
                discord.Embed(
                    title=f"{nation}'s membership status in the World Assembly is: {text}."
                )
            ]
        case "wabadges":
            if text:
                return [
                    discord.Embed(
                        title=f"{nation}'s has the following badges from the world assembly {text}."
                    )
                ]
            else:
                return [discord.Embed(title=f"{nation}'s has no from the world assembly.")]
        case "wcensus":
            return [discord.Embed(title=f"{nation}'s mining industry ranks {text} in the world.")]
        case "zombie":
            return [discord.Embed(title="ERROR", description=data)]
