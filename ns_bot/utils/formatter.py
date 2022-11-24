
import discord
import xmltodict

from itertools import islice

def format_xml(data):
    dictionary = flatten(xmltodict.parse(data))
    dictionaries = split_dict(dictionary)
    return build_embeds(dictionaries)

def flatten(nested_dict, sep =' ', pre =''):
    return { pre + sep + key if pre else key : v
             for kkey, vvalue in nested_dict.items()
             for key, v in flatten(vvalue, sep, kkey).items()
             } if isinstance(nested_dict, dict) else { pre : nested_dict }

def split_dict(dictionary, size = 10):
    it = iter(dictionary)
    items = []
    for i in range(0, len(dictionary), size):
        items.append({key:dictionary[key] for key in islice(it,size)})
    return items
    
def build_embeds(dictionaries):
    embeds = []
    for i in range(len(dictionaries)):
        embed = discord.Embed()
        for key, value in dictionaries[i].items():
            embed.add_field(name = str(key), value = str(value))
        embeds.append(embed) 
    return embeds  