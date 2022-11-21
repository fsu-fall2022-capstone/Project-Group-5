import asyncio
from io import BytesIO

from aiohttp import ClientSession
from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_URL = "https://www.nationstates.net/images/"


async def generate_issue_newspaper(
    web_session: ClientSession,
    nation: str,
    currency: str,
    article_title: str,
    banner_1: str,
    banner_2: str,
    flag,
):
    results = []
    urls = [flag, f"newspaper/{banner_1}-1.jpg", f"newspaper/{banner_2}-2.jpg"]
    for url in urls:
        async with web_session.get(
            BASE_IMAGE_URL + url, headers={"User-Agent": "NS Discord Bot"}
        ) as response:
            results.append(Image.open(BytesIO(await response.content.read())))

    # TODO put these images in place
    flag_image = results[0].convert("RGB")
    new_flag_image = flag_image.resize((30, 20))

    banner_1_image = results[1]
    banner_2_image = results[2]

    top_paper = Image.open("ns_bot/data/newspaper-references/paper1.png")
    header_paper = Image.open("ns_bot/data/newspaper-references/paper2.png")
    header_paper.paste(new_flag_image, (35, 10))
    header_font = ImageFont.truetype("ns_bot/data/newspaper-references/UnifrakturCook-Bold.ttf", 25)
    paper_name = ImageDraw.Draw(header_paper)
    paper_name.text(
        (header_paper.width / 3, 10),
        f"The {nation} Chronicle",
        font=header_font,
        fill=(68, 68, 68),
    )
    currency_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 10)
    paper_name.text(
        (header_paper.width - 120, 10),
        f"1 {currency}",
        font=currency_font,
        fill=(68, 68, 68),
    )

    title_paper = Image.open("ns_bot/data/newspaper-references/paper4.png")
    title_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 30)
    headline = ImageDraw.Draw(title_paper)
    headline.text((35, 10), f"{article_title}", font=title_font, fill=(68, 68, 68))

    bottom_paper = Image.open("ns_bot/data/newspaper-references/paper5.png")

    total_height = top_paper.height + header_paper.height + title_paper.height + bottom_paper.height

    paper_template = Image.new("RGBA", (bottom_paper.width, total_height))
    paper_template.paste(top_paper, (0, 0))
    paper_template.paste(header_paper, (0, top_paper.height))
    paper_template.paste(title_paper, (0, top_paper.height + header_paper.height))
    paper_template.paste(bottom_paper, (0, total_height - bottom_paper.height))

    final_template = Image.new("RGBA", paper_template.size)
    final_template.paste(banner_1_image, (35, (total_height - bottom_paper.height) - 6))
    final_template.paste(
        banner_2_image,
        (bottom_paper.width - 175, (total_height - bottom_paper.height) - 6),
    )
    final_template.paste(paper_template, (0, 0), paper_template)
    final_template.show()
