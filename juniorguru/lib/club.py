import os
import asyncio
from functools import wraps

import discord


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None
JUNIORGURU_GUILD_NUM = 769966886598737931

CHANNELS_MAPPING = {
    'roboti': 797107515186741248,
    'práce-bot': 834443926655598592,
}

EMOJI_UPVOTES = ['👍', '❤️']
EMOJI_DOWNVOTES = ['👎']


class ClubClient(discord.Client):
    @property
    def juniorguru_guild(self):
        return self.get_guild(JUNIORGURU_GUILD_NUM)

    async def fetch_channel(self, channel_id):
        return super().fetch_channel(CHANNELS_MAPPING.get(channel_id, channel_id))


def discord_task(task):
    """
    Decorator, which turns given async function into a one-time synchronous Discord
    task.

    The wrapped function is expected to be async and it gets a Discord client instance
    as the first and only argument. The resulting function is synchronous and is
    expected to be called without any arguments.
    """
    @wraps(task)
    def wrapper():
        class Client(ClubClient):
            async def on_ready(self):
                await self.wait_until_ready()
                await task(self)
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
    return sum([reaction.count for reaction in reactions if reaction.emoji in EMOJI_UPVOTES])


def count_downvotes(reactions):
    return sum([reaction.count for reaction in reactions if reaction.emoji in EMOJI_DOWNVOTES])
