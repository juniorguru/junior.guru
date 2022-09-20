from functools import wraps
from operator import attrgetter

import discord

from juniorguru.lib import loggers
from juniorguru.lib.club import DISCORD_MUTATIONS_ENABLED


ONBOARDING_CATEGORY_NAME = '👋 Tipy pro tebe'

CHANNELS_PER_CATEGORY_LIMIT = 50

CHANNELS_PER_CATEGORY_EXCEPTION_CODE = 50035


logger = loggers.get(__name__)


def manage_categories(channel_operation):
    @wraps(channel_operation)
    async def wrapper(client, *args, **kwargs):
        category = sorted(filter(is_onboarding_category, client.juniorguru_guild.categories),
                          key=attrgetter('position'))[0]
        iteration = 1
        while True:
            logger.debug(f"Managing categories, iteration #{iteration}")
            altered_args = list(args) + [category]
            try:
                return await channel_operation(client, *altered_args, **kwargs)
            except discord.HTTPException as e:
                if e.code != CHANNELS_PER_CATEGORY_EXCEPTION_CODE:
                    raise

                # This is how the exception looks like:
                #
                #   discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
                #   In parent_id: Maximum number of channels in category reached (50)

                logger.info("Could not perform channel operation, given category is full")
                logger.debug("Updating channels cache")
                categories = filter(is_onboarding_category,
                                    await client.juniorguru_guild.fetch_channels())
                available_categories = sorted(filter(is_available_category, categories),
                                              key=attrgetter('position'))
                try:
                    category = available_categories[0]
                except IndexError:
                    position = min([category.position for category in categories])
                    logger.info(f"No available categories, creating a new one on position {position}")
                    if DISCORD_MUTATIONS_ENABLED:
                        category = await client.juniorguru_guild.create_category_channel(ONBOARDING_CATEGORY_NAME,
                                                                                         position=position)
                    else:
                        logger.warning('Discord mutations not enabled')
                        raise e
            iteration += 1
    return wrapper


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
