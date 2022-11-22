from datetime import date
from io import BytesIO

from aiohttp import ClientSession
from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE_URL = "https://www.nationstates.net/images/"
LIGHT_BLACK = (68, 68, 68)


async def generate_issue_newspaper(
    web_session: ClientSession,
    nation: str,
    currency: str,
    article_title: str,
    banner_1: str,
    banner_2: str,
    flag: str,
    issue_number: str,
):
    top_paper = Image.open("ns_bot/data/newspaper-references/paper1.png")
    header_paper = Image.open("ns_bot/data/newspaper-references/paper2.png").convert("RGBA")
    bottom_paper_original = Image.open("ns_bot/data/newspaper-references/paper5.png").convert(
        "RGBA"
    )
    title_paper = Image.open("ns_bot/data/newspaper-references/paper4.png")
    TOTAL_HEIGHT = (
        top_paper.height + header_paper.height + title_paper.height + bottom_paper_original.height
    )

    verdana_font = ImageFont.truetype("ns_bot/data/newspaper-references/verdana.ttf", 12)
    header_font = ImageFont.truetype("ns_bot/data/newspaper-references/UnifrakturCook-Bold.ttf", 25)
    currency_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 10)
    title_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 30)

    results = []
    for url in [flag, f"newspaper/{banner_1}-1.jpg", f"newspaper/{banner_2}-2.jpg"]:
        async with web_session.get(
            BASE_IMAGE_URL + url, headers={"User-Agent": "NS Discord Bot"}
        ) as response:
            results.append(Image.open(BytesIO(await response.content.read())))

    flag_image = results[0]
    banner_1_image = results[1]
    banner_2_image = results[2]

    header_paper.paste(flag_image, (35, 10))

    header_draw_paper = ImageDraw.Draw(header_paper)
    header_draw_paper.line((header_paper.width - 63, 45, 35, 45), fill=LIGHT_BLACK, width=7)
    header_draw_paper.line(
        (header_paper.width - 63, header_paper.height, 35, header_paper.height),
        fill=LIGHT_BLACK,
        width=5,
    )

    header_draw_paper.text(
        (35, header_paper.height - 19), "CITY FINAL", font=verdana_font, fill=LIGHT_BLACK
    )
    header_draw_paper.text(
        ((header_paper.width / 3) + 20, header_paper.height - 19),
        date.today().strftime("%A %B %d, %Y"),
        font=verdana_font,
        fill=LIGHT_BLACK,
    )
    header_draw_paper.text(
        (header_paper.width - 172, header_paper.height - 19),
        f"VOL 32 NO. {issue_number}",
        font=verdana_font,
        fill=LIGHT_BLACK,
    )
    header_draw_paper.text(
        (header_paper.width / 3, 10), f"The {nation} Chronicle", font=header_font, fill=LIGHT_BLACK,
    )
    header_draw_paper.text(
        (header_paper.width - 120, 10), f"1 {currency}", font=currency_font, fill=LIGHT_BLACK,
    )

    for i in range(99):
        if title_font.getsize(article_title)[0] >= (title_paper.width - 65):
            title_font = ImageFont.truetype(
                "ns_bot/data/newspaper-references/times new roman.ttf", 30 - i
            )
            continue
        if title_font.getsize(article_title)[0] < (title_paper.width - 65):
            break
    headline = ImageDraw.Draw(title_paper)
    headline.text((35, 10), f"{article_title}", font=title_font, fill=LIGHT_BLACK)

    bottom_paper = bottom_paper_original.copy()

    bottom_paper.paste(banner_1_image, (35, -6))
    bottom_paper.paste(
        banner_2_image, (bottom_paper.width - 175, -6),
    )
    bottom_paper.paste(bottom_paper_original, (0, 0), bottom_paper_original)

    newspaper = Image.new("RGBA", (bottom_paper.width, TOTAL_HEIGHT))
    newspaper.paste(top_paper, (0, 0))
    newspaper.paste(header_paper, (0, top_paper.height))
    newspaper.paste(title_paper, (0, top_paper.height + header_paper.height))
    newspaper.paste(bottom_paper, (0, TOTAL_HEIGHT - bottom_paper.height))

    return newspaper
