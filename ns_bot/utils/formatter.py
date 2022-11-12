import discord
import xmltodict
import xml.etree.ElementTree as ET

def format_embed_tree(data):
    try:
        root = ET.fromstring(data)
        embed = discord.Embed(title=root.tag)
        for element in root.iter():
            embed.add_field (name=element.tag, value=element.attrib)
        return embed
    except:
        print('Unable to parse data')
        return discord.Embed(title='ERROR',description='XML PARSING ERROR OCCURRED')
