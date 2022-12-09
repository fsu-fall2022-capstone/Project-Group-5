import xml.etree.ElementTree as ET
from io import BytesIO

import discord
from PIL import Image, ImageDraw

from ns_bot.DAOs.nationstates_api import NationStatesAPI
from ns_bot.formatting import Formatter


class FormatIssueResponse(Formatter):
    @classmethod
    async def format(
        cls, nationstates_api: NationStatesAPI, channel: discord.TextChannel, response: str
    ) -> None:
        root: ET.Element = await cls.async_xml_parse(response)
        issue_root = root[0]

        result_embed = discord.Embed(title=issue_root.findtext("DESC"))

        if reclassifications := issue_root.find("RECLASSIFICATIONS"):
            result_embed.add_field(
                name="Nation has been reclassified.",
                value=ET.tostring(reclassifications),
            )

        headlines = "\n".join(
            [headline.text for headline in root[0].find("HEADLINES").findall("HEADLINE")]
        )
        result_embed.add_field(name="Headlines", value=headlines or "Nothing interesting")
        result_embed.add_field(
            name="Picked option", value=f"Option {int(issue_root.attrib.get('choice')) + 1} won"
        )

        await channel.send(
            embed=result_embed, file=cls.add_rankings(result_embed, issue_root.find("RANKINGS"))
        )

        if unlocks := issue_root.find("UNLOCKS"):
            banners = [banner.text for banner in unlocks.findall("BANNER")]
            file = await cls.get_banner_images(banners, nationstates_api)
            unlock_embed = discord.Embed(title="Unlocks")
            unlock_embed.set_image(url="attachment://banner_images.png")
            await channel.send(embed=unlock_embed, file=file)

        if new_policies := issue_root.find("NEW_POLICIES"):
            for policy in new_policies.findall("POLICY"):
                policy_embed = discord.Embed(
                    title=f"New Policy : {policy.findtext('NAME')}",
                    color=discord.Color.brand_green(),
                )
                policy_embed.set_image(url=cls.BASE_BANNER_URL + policy.findtext("PIC"))
                policy_embed.add_field(name="Category", value=policy.findtext("CAT"))
                policy_embed.add_field(name="Description", value=policy.findtext("DESC"))
                await channel.send(embed=policy_embed)

        if removed_policies := issue_root.find("REMOVED_POLICIES"):
            for policy in removed_policies.findall("POLICY"):
                policy_embed = discord.Embed(
                    title=f"Removed Policy : {policy.findtext('NAME')}",
                    color=discord.Color.brand_red(),
                )
                policy_embed.set_image(url=cls.BASE_BANNER_URL + policy.findtext("PIC"))
                policy_embed.add_field(name="Category", value=policy.findtext("CAT"))
                policy_embed.add_field(name="Description", value=policy.findtext("DESC"))
                await channel.send(embed=policy_embed)

    @classmethod
    def add_rankings(cls, embed: discord.Embed, rankings: ET.Element):
        ranks = rankings.findall("RANK")
        ranks.sort(key=lambda x: -float(x.findtext("PCHANGE")))
        change_image = Image.new(
            mode="RGBA", size=(157 * 7, (-(-len(ranks) // 7)) * 40), color=(47, 49, 54)
        )
        for i, rank in enumerate(ranks):
            change_image.paste(cls.scale_to_image(rank), (157 * (i % 7), (i // 7) * 40))

        image_file = BytesIO()
        change_image.save(image_file, format="PNG")
        image_file.seek(0)
        embed.set_image(url="attachment://change.png")
        return discord.File(image_file, filename="change.png")

    @classmethod
    async def get_banner_images(cls, banners: list[str], nationstates_api: NationStatesAPI):
        banner_urls = [f"banners/{banner}" for banner in banners][: cls.IMAGE_LIMIT]
        image_results: list[Image.Image] = await nationstates_api.get_banners(banner_urls)

        list_length = len(image_results)
        w = image_results[0].width
        h = image_results[0].height
        half_len = -(-list_length // 2)

        compiled_banners_image = Image.new(
            mode="RGB", size=(w * 2, h * (half_len)), color=(47, 49, 54)
        )

        for i, banner in enumerate(image_results):
            # left column
            if i < list_length:
                compiled_banners_image.paste(banner, (0, h * i))
            # right column
            compiled_banners_image.paste(banner, (w, h * (i - half_len)))

        image_file = BytesIO()
        compiled_banners_image.save(image_file, format="PNG")
        image_file.seek(0)
        return discord.File(image_file, filename="banner_images.png")

    @staticmethod
    def scale_to_image(scale: ET.Element):
        id = scale.attrib.get("id")
        rank_image = Image.open(f"ns_bot/data/ranks/{id}.png")
        change_image = Image.new(
            mode="RGBA", size=(int(rank_image.width * 3.5), rank_image.height), color=(47, 49, 54)
        )
        change_image.paste(rank_image, (0, 0))
        add_text_to_image = ImageDraw.Draw(change_image)
        if float(scale.findtext("CHANGE")) > 0:
            fill = (50, 255, 74)
        else:
            fill = (255, 74, 50)
        add_text_to_image.text((rank_image.width + 5, 3), scale.findtext("SCORE"), fill=fill)
        add_text_to_image.text((rank_image.width + 5, 15), scale.findtext("CHANGE"), fill=fill)
        add_text_to_image.text(
            (rank_image.width + 5, 29), f"{scale.findtext('PCHANGE')}%", fill=fill
        )
        return change_image
