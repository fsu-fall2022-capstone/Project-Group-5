import asyncio
import os
import sys

import requests
from aiohttp import ClientSession
from PIL import Image, ImageDraw, ImageFont

nation_name = "NATION"
nation_currency = "CURRENCY"
article_title = "Title Here!"

image_url = "https://www.nationstates.net/images/"


async def get_images():
    results = []
    urls = [
        "flags/uploads/computer_chip__602300t1.png",
        "newspaper/t1-1.jpg",
        "newspaper/s1-2.jpg",
    ]
    async with ClientSession() as session:
        for url in urls:
            async with session.get(image_url + url) as response:
                results.append(await response.text())
        flag_image = results[0]
        big_paper_image = results[1]
        small_paper_image = results[2]
    return results


results = asyncio.run(get_images())

top_paper = Image.open("ns_bot/data/newspaper-references/dpaper1.png")

header_paper = Image.open("ns_bot/data/newspaper-references/dpaper2.png")
header_font = ImageFont.truetype(
    "ns_bot/data/newspaper-references/UnifrakturCook-Bold.ttf", 25
)
paper_name = ImageDraw.Draw(header_paper)
paper_name.text(
    (header_paper.width / 3, 10),
    f"The {nation_name} Chronicle",
    font=header_font,
    fill=(68, 68, 68),
)
currency_font = ImageFont.truetype(
    "ns_bot/data/newspaper-references/times new roman.ttf", 10
)
paper_name.text(
    (header_paper.width - 120, 10),
    f"1 {nation_currency}",
    font=currency_font,
    fill=(68, 68, 68),
)

title_paper = Image.open("ns_bot/data/newspaper-references/dpaper4.png")
title_font = ImageFont.truetype(
    "ns_bot/data/newspaper-references/times new roman.ttf", 50
)
headline = ImageDraw.Draw(title_paper)
headline.text((35, 10), f"{article_title}", font=title_font, fill=(68, 68, 68))

bottom_paper = Image.open("ns_bot/data/newspaper-references/dpaper5.png")

total_height = (
    top_paper.height + header_paper.height + title_paper.height + bottom_paper.height
)

paper_template = Image.new("RGBA", (bottom_paper.width, total_height))
paper_template.paste(top_paper, (0, 0))
paper_template.paste(header_paper, (0, top_paper.height))
paper_template.paste(title_paper, (0, top_paper.height + header_paper.height))
paper_template.paste(bottom_paper, (0, total_height - bottom_paper.height))

paper_template.show()
# nation_name
# nation_city
# nation_flag
# nation_currency
# download static images for newspaper
# write headline of newspaper
# flag, first, and second banner are variable, call from website itself

# "draw" newspaper together using amalgamation
# making a file but dont want to save: import io
# font-family: unifrakturcook,times new roman,serif;
