import re
import os
import asyncio
from functools import wraps

import discord


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None
DISCORD_MUTATIONS_ENABLED = bool(int(os.getenv('DISCORD_MUTATIONS_ENABLED', 0)))
JUNIORGURU_GUILD_NUM = 769966886598737931

CHANNELS_MAPPING = {
    'roboti': 797107515186741248,
    'práce-bot': 834443926655598592,
    'moderátoři': 788822884948770847,
    'meta': 806215364379148348,
}

DEFAULT_EXCLUDED_CATEGORIES = [
    r'\bcoreskill\b',  # CoreSkill's internal mentoring channels
]
DEFAULT_EXCLUDED_CHANNELS = [
    r'\broboti\b',
    r'\bmoderátoři\b',
]
DEFAULT_EXCLUDED_MEMBERS = [
    668226181769986078,  # Honza Javorek
    797097976571887687,  # kuře
]

EMOJI_UPVOTES = ['👍', '❤️', '😍', '🥰', '💕', '♥️', '💖', '💙', '💗', '💜', '💞', '💓', '💛', '🖤', '💚', '😻', '🧡', '👀',
                 '💯', '🤩', '😋', '💟', '🤍', '🤎', '💡', '👆', '👏', '🥇', '🏆', '✔️', 'plus_one', '👌', 'babyyoda',
                 'meowthumbsup', '✅', '🤘', 'this']
EMOJI_DOWNVOTES = ['👎']


class BaseClient(discord.Client):
    @property
    def juniorguru_guild(self):
        return self.get_guild(JUNIORGURU_GUILD_NUM)

    async def fetch_channel(self, channel_id):
        return await super().fetch_channel(translate_channel_id(channel_id))


def discord_task(task):
    """
    Decorator, which turns given async function into a one-time synchronous Discord
    task.

    The wrapped function is expected to be async and it gets a Discord client instance
    as the first argument. The resulting function is synchronous. Any arguments given
    to the resulting function get passed down to the wrapped function. Positional
    arguments follow after the client instance.
    """
    @wraps(task)
    def wrapper(*args, **kwargs):
        class Client(BaseClient):
            async def on_ready(self):
                await self.wait_until_ready()
                await task(self, *args, **kwargs)
                await self.close()

            async def on_error(self, event, *args, **kwargs):
                raise

        intents = discord.Intents(guilds=True, members=True)
        client = Client(loop=asyncio.new_event_loop(), intents=intents)

        exc = None
        def exc_handler(loop, context):
            nonlocal exc
            exc = context.get('exception')
            loop.default_exception_handler(context)
            loop.stop()

        client.loop.set_exception_handler(exc_handler)
        client.run(DISCORD_API_KEY)

        if exc:
            raise exc
    return wrapper


def translate_channel_id(channel_id):
    return CHANNELS_MAPPING.get(channel_id, channel_id)


def count_upvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_UPVOTES])


def count_downvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_DOWNVOTES])


# '🆗'
# <PartialEmoji animated=False name='lolpain' id=764265678810382366>
# <PartialEmoji animated=False name='BabyYoda' id=802415790010794016>
def emoji_name(emoji):
    try:
        return emoji.name.lower()
    except AttributeError:
        return str(emoji)


def exclude_categories(channels, categories=None):
    categories = categories or DEFAULT_EXCLUDED_CATEGORIES
    if not categories:
        raise ValueError('Empty list of categories')
    exclude_categories_re = re.compile(r'|'.join(categories), re.IGNORECASE)
    return (channel for channel in channels
            if not channel.category or not exclude_categories_re.search(channel.category.name))


def exclude_channels(channels, channels_to_exclude=None):
    channels_to_exclude = channels_to_exclude or DEFAULT_EXCLUDED_CHANNELS
    if not channels_to_exclude:
        raise ValueError('Empty list of channels')
    exclude_channels_re = re.compile(r'|'.join(channels_to_exclude), re.IGNORECASE)
    return (channel for channel in channels
            if not exclude_channels_re.search(channel.name))


def exclude_bots(members):
    return (member for member in members if not member.bot)


def exclude_members(members, members_to_exclude=None):
    members_to_exclude = members_to_exclude or DEFAULT_EXCLUDED_MEMBERS
    if not members:
        raise ValueError('Empty list of members')
    return (member for member in members
            if member.id not in members_to_exclude)


def is_default_avatar(url):
    return bool(re.search(r'/embed/avatars/\d+\.', url))


def get_roles(member_or_user):
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]
