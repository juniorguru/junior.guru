import re
import os
import asyncio
from functools import wraps

import discord


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None
DISCORD_MUTATIONS_ENABLED = bool(int(os.getenv('DISCORD_MUTATIONS_ENABLED', 0)))
JUNIORGURU_GUILD = 769966886598737931

EMOJI_UPVOTES = ['👍', '❤️', '😍', '🥰', '💕', '♥️', '💖', '💙', '💗', '💜', '💞', '💓', '💛', '🖤', '💚', '😻', '🧡', '👀',
                 '💯', '🤩', '😋', '💟', '🤍', '🤎', '💡', '👆', '👏', '🥇', '🏆', '✔️', 'plus_one', '👌', 'babyyoda',
                 'meowthumbsup', '✅', '🤘', 'this', 'dk', '🙇‍♂️', '🙇', '🙇‍♀️', 'kgsnice', 'successkid', 'white_check_mark',
                 'notbad']
EMOJI_DOWNVOTES = ['👎']
EMOJI_PINS = ['📌']


class BaseClient(discord.Client):
    @property
    def juniorguru_guild(self):
        return self.get_guild(JUNIORGURU_GUILD)


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


def count_upvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_UPVOTES])


def count_downvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_DOWNVOTES])


def count_pins(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_PINS])


def emoji_name(emoji):
    try:
        return emoji.name.lower()
    except AttributeError:
        return str(emoji)


def is_default_avatar(url):
    return bool(re.search(r'/embed/avatars/\d+\.', str(url)))


def get_roles(member_or_user):
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]
