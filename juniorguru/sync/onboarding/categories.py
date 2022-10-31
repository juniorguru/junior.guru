import math
from operator import attrgetter

import discord

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED


ONBOARDING_CATEGORY_NAME = '👋 Tipy pro tebe'

CHANNELS_PER_CATEGORY_LIMIT = 50

CHANNELS_PER_CATEGORY_EXCEPTION_CODE = 50035


logger = loggers.from_path(__file__)


async def manage_category(guild, async_fn):
    category = get_available_category(guild.categories)  # from cache
    while True:
        try:
            return await async_fn(category)
        except discord.HTTPException as e:
            if e.code != CHANNELS_PER_CATEGORY_EXCEPTION_CODE:
                raise
            logger.info(f"Category #{category.id} is full")
            category = get_available_category(await guild.fetch_channels())  # fresh fetch


class NoOnboardingCategoriesAvailableError(Exception):
    pass


def get_available_category(channels):
    categories = sorted(filter(is_available_category, channels),
                        key=attrgetter('position'))
    try:
        return categories[0]
    except IndexError:
        raise NoOnboardingCategoriesAvailableError()


async def create_enough_categories(client, max_channels_needed):
    categories = list(filter(is_onboarding_category,
                             await client.juniorguru_guild.fetch_channels()))
    logger.info(f"Found {len(categories)} existing categories, maximum {max_channels_needed} channels will be needed")
    missing_categories_count = calc_missing_categories_count(len(categories), max_channels_needed)
    if missing_categories_count:
        logger.info(f"Creating {missing_categories_count} categories to have enough of them even for the worst case scenario")
        position = min([category.position for category in categories])
        if DISCORD_MUTATIONS_ENABLED:
            for _ in range(missing_categories_count):
                await client.juniorguru_guild.create_category_channel(ONBOARDING_CATEGORY_NAME,                                                          position=position)
        else:
            logger.warning('Discord mutations not enabled')


def calc_missing_categories_count(existing_categories_count, max_channels_needed):
    max_categories_needed = math.ceil(max_channels_needed / CHANNELS_PER_CATEGORY_LIMIT)
    return max(max_categories_needed - existing_categories_count, 0)


async def delete_empty_categories(client):
    categories = (channel for channel
                  in (await client.juniorguru_guild.fetch_channels())
                  if is_onboarding_category(channel) and has_no_channels(channel))
    for category in categories:
        logger.info("Found onboarding category with no channels, deleting")
        if DISCORD_MUTATIONS_ENABLED:
            await category.delete()
        else:
            logger.warning('Discord mutations not enabled')


def is_onboarding_category(channel):
    return (channel.type == discord.ChannelType.category and
            channel.name == ONBOARDING_CATEGORY_NAME)


def is_available_category(channel):
    return (is_onboarding_category(channel) and
            len(channel.channels) < CHANNELS_PER_CATEGORY_LIMIT)


def has_no_channels(channel):
    return (is_onboarding_category(channel) and
            len(channel.channels) == 0)
