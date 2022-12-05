from datetime import date
from io import BytesIO

from aiohttp import ClientSession
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.ImageFont import FreeTypeFont
from cairosvg import svg2png

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
    bottom_paper_template = Image.open("ns_bot/data/newspaper-references/paper5.png").convert(
        "RGBA"
    )
    title_paper = Image.open("ns_bot/data/newspaper-references/paper4.png")
    TOTAL_HEIGHT = (
        top_paper.height + header_paper.height + title_paper.height + bottom_paper_template.height
    )

    verdana_font = ImageFont.truetype("ns_bot/data/newspaper-references/verdana.ttf", 12)
    header_font = ImageFont.truetype("ns_bot/data/newspaper-references/UnifrakturCook-Bold.ttf", 25)
    currency_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 10)
    title_font = ImageFont.truetype("ns_bot/data/newspaper-references/times new roman.ttf", 50)

    # Make sure the article title fits the image
    title_font_size = 50
    while title_font_size > 1 and title_font.getlength(article_title) >= (title_paper.width - 98):
        title_font_size -= 1
        title_font = ImageFont.truetype(
            "ns_bot/data/newspaper-references/times new roman.ttf", title_font_size
        )

    results = []

    if flag.endswith(".svg"):
        flag = Image.open(BytesIO(svg2png(url=BASE_IMAGE_URL + flag, write_to=None)))
        for url in [f"newspaper/{banner_1}-1.jpg", f"newspaper/{banner_2}-2.jpg"]:
            async with web_session.get(
                BASE_IMAGE_URL + url, headers={"User-Agent": "NS Discord Bot"}
            ) as response:
                results.append(Image.open(BytesIO(await response.content.read())))
        flag_image: Image.Image = flag
        banner_1_image: Image.Image = results[0]
        banner_2_image: Image.Image = results[1]
    else:
        for url in [flag, f"newspaper/{banner_1}-1.jpg", f"newspaper/{banner_2}-2.jpg"]:
            async with web_session.get(
                BASE_IMAGE_URL + url, headers={"User-Agent": "NS Discord Bot"}
            ) as response:
                results.append(Image.open(BytesIO(await response.content.read())))
        flag_image: Image.Image = results[0]
        banner_1_image: Image.Image = results[1]
        banner_2_image: Image.Image = results[2]

    flag_image = ImageOps.contain(flag_image, (50, 30))
    header_paper.paste(flag_image, (38, 10))

    header_draw_paper = ImageDraw.Draw(header_paper)
    header_draw_paper.line((header_paper.width - 62, 45, 38, 45), fill=LIGHT_BLACK, width=7)
    header_draw_paper.line(
        (header_paper.width - 62, header_paper.height, 38, header_paper.height),
        fill=LIGHT_BLACK,
        width=5,
    )

    header_draw_paper.text(
        (38, header_paper.height - 19), "CITY FINAL", font=verdana_font, fill=LIGHT_BLACK
    )
    date_string = date.today().strftime("%A %B %d, %Y")
    header_draw_paper.text(
        (
            get_left_corner_for_center(
                verdana_font,
                date_string,
                header_paper.width,
            ),
            header_paper.height - 19,
        ),
        date_string,
        font=verdana_font,
        fill=LIGHT_BLACK,
    )
    header_draw_paper.text(
        (header_paper.width - 166, header_paper.height - 19),
        f"VOL 32 NO. {issue_number}",
        font=verdana_font,
        fill=LIGHT_BLACK,
    )
    nation_string = f"The {nation} Chronicle"
    header_draw_paper.text(
        (
            get_left_corner_for_center(
                header_font,
                nation_string,
                header_paper.width,
            ),
            10,
        ),
        nation_string,
        font=header_font,
        fill=LIGHT_BLACK,
    )
    header_draw_paper.text(
        (header_paper.width - 120, 10),
        f"1 {currency}",
        font=currency_font,
        fill=LIGHT_BLACK,
    )

    headline = ImageDraw.Draw(title_paper)

    headline.text(
        (35, (title_paper.height - title_font.getsize(article_title)[1]) / 2),
        f"{article_title}",
        font=title_font,
        fill=LIGHT_BLACK,
    )

    bottom_paper = bottom_paper_template.copy()

    banner_1_image = banner_1_image.resize((411, 114), Image.ANTIALIAS)
    banner_2_image = banner_2_image.resize((104, 114), Image.ANTIALIAS)
    bottom_paper.paste(banner_1_image, (38, 4))
    bottom_paper.paste(
        banner_2_image,
        (bottom_paper.width - 166, 3),
    )
    bottom_paper.paste(bottom_paper_template, (0, 0), bottom_paper_template)

    newspaper = Image.new("RGBA", (bottom_paper.width, TOTAL_HEIGHT))
    newspaper.paste(top_paper, (0, 0))
    newspaper.paste(header_paper, (0, top_paper.height))
    newspaper.paste(title_paper, (0, top_paper.height + header_paper.height))
    newspaper.paste(bottom_paper, (0, TOTAL_HEIGHT - bottom_paper.height))

    return newspaper


def get_left_corner_for_center(font: FreeTypeFont, string: str, total_width: int):
    total_width = total_width - 108
    return ((total_width - font.getlength(string)) / 2) + 45
