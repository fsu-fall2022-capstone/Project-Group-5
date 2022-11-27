
import discord
import xml.etree.ElementTree as ET

from ns_bot.utils.wrappers import async_wrapper

async def format_nation_info(data:str, shard):
    
    async_parse = async_wrapper(ET.fromstring)
    root = await async_parse(data)  
    nation = ' '.join(root.attrib['id'].title().split('_'))
    text = root[0].text
    color = discord.Color.random()
    national_currency = "UNKNOWN currency"
    if shard:
        match shard:
            case 'admirable':
                return [discord.Embed(title=f"The people of {nation} are well-known for being very {text}.", color=color)]
            case 'admirables':
                traits = ''
                for i in range(0, len(root[0])):
                    if i == 0:
                        traits = traits + root[0][i].text
                    elif i == len(root[0]) - 1:
                        traits = traits + ", and " + root[0][i].text
                    else:
                        traits = traits + ", " + root[0][i].text
                return [discord.Embed(title=f"The people of {nation} are known to be {traits}.", color=color)]
            case 'animal':
                return [discord.Embed(title=f"{nation}'s national animal is the: {text.title()}", color=color)]
            case 'animaltrait':
                return [discord.Embed(title=f"The national animal of {nation} {text}.", color=color)]
            case 'answered':
                return [discord.Embed(title=f"{nation} has voted on {text} issues", color=color)]
            case 'banner':
                pass
            case 'banners':
                pass
            case 'capital':
                return [discord.Embed(title=f"{text.title()} is the capital city of {nation} ", color=color)]
            case 'category':
                return [discord.Embed(title=f"{nation} is a {text}!", color=color)]
            case 'census':
                embed=discord.Embed(title=f"{nation}'s Public Education standing", color=color)
                embed.add_field(name="World Ranking", value=root[0][0][1].text, inline=False)
                embed.add_field(name="Rank within the Region", value=root[0][0][2].text, inline=False)
                embed.add_field(name="Score on the ", value=root[0][0][0].text, inline=False)
                return [embed]
            case 'crime':
                return [discord.Embed(title=f"{text.capitalize()}", color=color)]
            case 'currency':
                return [discord.Embed(title=f"The {text.capitalize()} is the national currency of {nation}", color=color)]
            case 'customleader':
                return [discord.Embed(title="ERROR", description=data)]
            case 'customcapital':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'customreligion':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'dbid':
                return [discord.Embed(title=f"Database ID for {nation}: {text}", color=color)]
            case 'deaths':
                embed=discord.Embed(title=f"Causes of death in {nation}", color=color)
                for cause in root[0].iterfind('CAUSE'):
                    embed.add_field(name=f"{cause.text}% of people die from:", value=f"{cause.attrib['type']}", inline=False)
                return [embed]
            case 'demonym':
                return [discord.Embed(title=f"A person from {nation} is a {text}", color=color)]
            case 'demonym2':
                return [discord.Embed(title=f"Another common name for a person from {nation} is {text}", color=color)]
            case 'demonym2plural':
                return [discord.Embed(title=f"A group of people from {nation} are called {text}", color=color)]
            case 'dispatches':
                return [discord.Embed(title=f"{nation} has had {text} dispatches", color=color)]
            case 'dispatchlist':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'endorsements':
                if text:
                    return [discord.Embed(title=f"{nation} has been endorsed by {len(root[0].findall('ENDORSEMENT'))} nations", color=color)]
                else:
                    return [discord.Embed(title=f"{nation} has been endorsed by zero nations!", color=color)] 
            case 'factbooks':
                return [discord.Embed(title=f"{nation} has a total of {text} factbooks written about them.", color=color)]
            case 'factbooklist':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'firstlogin':
                return [discord.Embed(title=f"The nation of {nation} was first logged in on {text}.", color=color)]
            case 'flag':
                embed = discord.Embed(title=f"The flag of {nation}", url=text, color=color)
                return [embed]
            case 'founded':
                return [discord.Embed(title=f"{nation} was founded exactly {text}!", color=color)]
            case 'foundedtime':
                return [discord.Embed(title=f"The nation of {nation} was founded at {text}.", color=color)]
            case 'freedom':
                sentence = f"The nation of {nation} has a {root[0][0].text.lower()} record of civil rights, an economy considered by many to be {root[0][1].text.lower()}, and a political system that is {root[0][2].text.lower()}."
                return [discord.Embed(title=sentence, color=color)]
            case 'fullname':
                return [discord.Embed(title=f"The proper name of {nation} is '{text}'.", color=color)]
            case 'gavote':
                return [discord.Embed(title=f"{nation}'s status in the General Assembly is currently {text}.", color=color)]
            case 'gdp':
                return [discord.Embed(title=f"The nation of {nation} has a GDP of {text} {national_currency}!", color=color)]
            case 'govt':
                pass
            case 'govtdesc':
                return [discord.Embed(title=text, color=color)]
            case 'govtpriority':
                return [discord.Embed(title=f"The government of {nation} prioritizes their {text} above all else.", color=color)]
            case 'happenings':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'income':
                return [discord.Embed(title=f"The average income for a resident of {nation} is {text} {national_currency}.", color=color)]
            case 'industrydesc':
                return [discord.Embed(title=text, color=color)]
            case 'influence':
                return [discord.Embed(title=f"The nation of {nation} spreads its influence by being a {text}.", color=color)]
            case 'lastactivity':
                return [discord.Embed(title=f"{nation} had their most recent activity {text}.", color=color)]
            case 'lastlogin':
                return [discord.Embed(title=f"{nation} was last logged in {text}.", color=color)]
            case 'leader':
                return [discord.Embed(title=f"{text} is the current leader of {nation}.", color=color)]
            case 'legislation':
                return [discord.Embed(title="ERROR", description=data, color=color)]
            case 'majorindustry':
                return [discord.Embed(title=f"{text} is the biggest industry of {nation}!", color=color)]
            case 'motto':
                return [discord.Embed(title=f'"{text}"' + f" is the motto of {nation}.", color=color)]
            case 'name':
                return [discord.Embed(title=nation, color=color)]
            case 'notable':
                return [discord.Embed(title=f"{nation} is known for their {text}.", color=color)]
            case 'notables':
                pass
            case 'policies':
                pass
            case 'poorest':
                return [discord.Embed(title=f"The poorest 10% of people in {nation} have a reported income of  {text} {national_currency}.", color=color)]
            case 'population':
                if len(text) < 4:
                    return [discord.Embed(title=f"{nation} has a population of {text} million", color=color)]
                else:
                    return [discord.Embed(title=f"{nation} has a population of {float(text) / 1000} billion.", color=color)]
            case 'publicsector':
                return [discord.Embed(title=f"{text}% of {nation}'s economy is controlled by it's government.", color=color)]
            case 'rcensus':
                pass
            case 'region':
                return [discord.Embed(title=f"{nation} can be found in the {text} region.", color=color)]
            case 'religion':
               return [discord.Embed(title=f"{text} is the official religion of {nation}.", color=color)]
            case 'richest':
                return [discord.Embed(title=f"The richest 10% of people in {nation} have a reported income of  {text} {national_currency}.", color=color)]
            case 'scvote':
                if text:
                    return [discord.Embed(title=f"{nation}'s status on the Security Council is currently {text}.", color=color)]
                else:
                    return [discord.Embed(title=f"{nation} is not a member of the Security Council.", color=color)]
            case 'sectors':
                pass
            case 'sensibilities':
                return [discord.Embed(title=f"The people of {nation} are known to be {text}.", color=color)]
            case 'tax':
                return [discord.Embed(title=f"The average tax rate in {nation} is {text}%.", color=color)]
            case 'tgcanrecruit':
                if text == '1':
                    return [discord.Embed(title=f"{nation} can receive recruitment telegrams.", color=color)]
                else:
                    return [discord.Embed(title=f"{nation} can not receive recruitment telegrams.", color=color)]
            case 'tgcancampaign':
                if text == '1':
                    return [discord.Embed(title=f"{nation} can receive campaign telegrams.", color=color)]
                else:
                    return [discord.Embed(title=f"{nation} can not receive campaign telegrams.", color=color)]
            case 'type':
                return [discord.Embed(title=f"{nation} is a {text}!", color=color)]
            case 'wa':
                return [discord.Embed(title=f"{nation}'s membership status in the World Assmeby is: {text}.", color=color)]
            case 'wabadges':
                if text:
                    return [discord.Embed(title=f"{nation}'s has the following badges from the world assembly {text}.", color=color)]
                else:
                    return [discord.Embed(title=f"{nation}'s has no from the world assembly.", color=color)]
            case 'wcensus':
                return [discord.Embed(title=f"{nation}'s mining industry ranks {text} in the world.", color=color)]
            case 'zombie':
                pass
    else:
        return [discord.Embed(title="Nation Info", description=data)]

def format_region_info(data,shard):
    return discord.Embed(title="Region Info", description=data)