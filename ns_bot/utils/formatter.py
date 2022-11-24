import discord
import xmltodict

def format_xml(data):
    dictionary = xmltodict.parse(data)
    return build_embed(discord.Embed(), dictionary)

def build_embed(embed, dictionary):
    for key, value in dictionary.items():
        if isinstance(value,dict):
            build_embed(embed, value)
        else:    
            embed.add_field(name = str(key), value = str(value)) 
    return embed     

