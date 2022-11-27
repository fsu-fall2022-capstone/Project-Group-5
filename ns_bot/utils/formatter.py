
import discord
import random
import xml.etree.ElementTree as ET

from ns_bot.data.shards import VALID_PUBLIC_NATION_SHARDS
from ns_bot.utils.wrappers import async_wrapper

async def format_nation_info(data, shard):
    
    async_parse = async_wrapper(ET.fromstring)
    root = await async_parse(data)
    if shard:
        match shard:
            case 'admirable':
                print(len(VALID_PUBLIC_NATION_SHARDS))
                return [discord.Embed(title=f"{root.attrib['id'].capitalize()}'s top trait is being {root[0].text.capitalize()}", color=discord.Color.dark_red())]
            case 'admirables':
                embed=discord.Embed(title=f"Admirable Traits of {root.attrib['id'].capitalize()}", color=discord.Color.green())
                for i in range(0, len(root[0])):
                    embed.add_field(name=f"Trait {i+1}",value=str(root[0][i].text.title()), inline=False)
                return [embed]
            case 'animal':
                return [discord.Embed(title=f"{root.attrib['id'].capitalize()}'s national animal is the: {root[0].text.title()}", color=discord.Color.blurple())]
            case 'animaltrait':
                return [discord.Embed(title=f"The national animal of {root.attrib['id'].capitalize()} has this trait:", description=f"{root[0].text.capitalize()}", color=discord.Color.blurple())]
            case 'answered':
                return [discord.Embed(title=f"{root.attrib['id'].capitalize()} has voted on {root[0].text.capitalize()} issues", color=discord.Color.gold())]
            case 'banner':
                pass
            case 'banners':
                pass
            case 'capital':
                return [discord.Embed(title=f"{root[0].text.title()} is the capital city of {root.attrib['id'].capitalize()} ", color=discord.Color.teal())]
            case 'category':
                return [discord.Embed(title=f"{root.attrib['id'].title()} is a {root[0].text} !", color=discord.Color.red())]
            case 'census':
                embed=discord.Embed(title=f"{root.attrib['id'].title()}'s Public Education standing", color=discord.Color.fuchsia())
                embed.add_field(name="World Ranking", value=root[0][0][1].text, inline=False)
                embed.add_field(name="Rank within the Region", value=root[0][0][2].text, inline=False)
                embed.add_field(name="Raw Score", value=root[0][0][0].text, inline=False)
                return [embed]
            case 'crime':
                return [discord.Embed(title=f"Criminal activity in {root.attrib['id'].title()}", description=f"{root[0].text.capitalize()}")]
            case 'currency':
                return [discord.Embed(title=f"The {root[0].text.capitalize()} is the national currency of {root.attrib['id'].title()}")]
            case 'customleader':
                return [discord.Embed(title="ERROR", description=data)]
            case 'customcapital':
                return [discord.Embed(title="ERROR", description=data)]
            case 'customreligion':
                return [discord.Embed(title="ERROR", description=data)]
            case 'dbid':
                return [discord.Embed(title=f"Database ID for {root.attrib['id'].title()}: {root[0].text}")]
            case 'deaths':
                embed=discord.Embed(title=f"People die for {root.attrib['id'].title()}: {root[0].text}")
                pass
            case 'demonym':
                pass
            case 'demonym2':
                pass
            case 'demonym2plural':
                pass
            case 'dispatches':
                pass
            case 'dispatchlist':
                pass
            case 'endorsements':
                pass
            case 'factbooks':
                pass
            case 'factbooklist':
                pass
            case 'firstlogin':
                pass
            case 'flag':
                pass
            case 'founded':
                pass
            case 'foundedtime':
                pass
            case 'freedom':
                pass
            case 'fullname':
                pass
            case 'gavote':
                pass
            case 'gdp':
                pass
            case 'govt':
                pass
            case 'govtdesc':
                pass
            case 'govtpriority':
                pass
            case 'happenings':
                pass
            case 'income':
                pass
            case 'industrydesc':
                pass
            case 'influence':
                pass
            case 'lastactivity':
                pass
            case 'lastlogin':
                pass
            case 'leader':
                pass
            case 'legislation':
                pass
            case 'majorindustry':
                pass
            case 'motto':
                pass
            case 'name':
                pass
            case 'notable':
                pass
            case 'notables':
                pass
            case 'policies':
                pass
            case 'poorest':
                pass
            case 'population':
                pass
            case 'publicsector':
                pass
            case 'rcensus':
                pass
            case 'region':
                pass
            case 'religion':
                pass
            case 'richest':
                pass
            case 'scvote':
                pass
            case 'sectors':
                pass
            case 'sensibilities':
                pass
            case 'tax':
                pass
            case 'tgcanrecruit':
                pass
            case 'tgcancampaign':
                pass
            case 'type':
                pass
            case 'wa':
                pass
            case 'wabadges':
                pass
            case 'wcensus':
                pass
            case 'zombie':
                pass
    else:
        return [discord.Embed(title="Nation Info", description=data)]

def format_region_info(data,shard):
    return discord.Embed(title="Region Info", description=shard)