import discord
from discord import app_commands
from discord.ext import commands

from controllers.base_controller import BaseController
from nationstates_bot import NationStatesBot


class BaseNationstateController(BaseController):
    VALID_PUBLIC_SHARDS = [
        'admirable',
        'admirables',
        'animal',
        'animaltrait',
        'answered',
        'banner',
        'banners',
        'capital',
        'category',
        'census',
        'crime',
        'currency',
        'customleader',
        'customcapital',
        'customreligion',
        'dbid',
        'deaths',
        'demonym',
        'demonym2',
        'demonym2plural',
        'dispatches',
        'dispatchlist',
        'endorsements',
        'factbooks',
        'factbooklist',
        'firstlogin',
        'flag',
        'founded',
        'foundedtime',
        'freedom',
        'fullname',
        'gavote',
        'gdp',
        'govt',
        'govtdesc',
        'govtpriority',
        'happenings',
        'income',
        'industrydesc',
        'influence',
        'lastactivity',
        'lastlogin',
        'leader',
        'legislation',
        'majorindustry',
        'motto',
        'name',
        'notable',
        'notables',
        'policies',
        'poorest',
        'population',
        'publicsector',
        'rcensus',
        'region',
        'religion',
        'richest',
        'scvote',
        'sectors',
        'sensibilities',
        'tax',
        'tgcanrecruit',
        'tgcancampaign',
        'type',
        'wa',
        'wabadges',
        'wcensus',
        'zombie',
    ]

    @classmethod
    async def public_shards_autocomplete(
        cls, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:

        options = [
            app_commands.Choice(name=valid, value=valid)
            for valid in cls.VALID_PUBLIC_SHARDS
            if current.lower() in valid.lower()
        ]
        options.sort(key=lambda x: x.name)
        return options[:25]
