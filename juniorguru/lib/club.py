import re
import os
import asyncio
from functools import wraps
from datetime import timedelta, date

import discord

from juniorguru.lib import loggers


DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None
DISCORD_MUTATIONS_ENABLED = bool(int(os.getenv('DISCORD_MUTATIONS_ENABLED', 0)))
JUNIORGURU_GUILD = 769966886598737931

EMOJI_PINS = ['📌']
EMOJI_UPVOTES = ['👍', '❤️', '😍', '🥰', '💕', '♥️', '💖', '💙', '💗', '💜', '💞', '💓', '💛', '🖤', '💚', '😻', '🧡', '👀',
                 '💯', '🤩', '😋', '💟', '🤍', '🤎', '💡', '👆', '👏', '🥇', '🏆', '✔️', 'plus_one', '👌', 'babyyoda',
                 'meowthumbsup', '✅', '🤘', 'this', 'dk', '🙇‍♂️', '🙇', '🙇‍♀️', 'kgsnice', 'successkid', 'white_check_mark',
                 'notbad', 'updoot', '🆒', '🔥'] + EMOJI_PINS
EMOJI_DOWNVOTES = ['👎']

COUPON_RE = re.compile(r'''
    ^
        (?P<coupon_name>
            (?P<student_prefix>STUDENT)?
            [A-Z]+
        )
        (?P<coupon_suffix>[0-9]+)
        (I(?P<invoice_id>[0-9]+))?
        (V(?P<version>[0-9]+))?
    $
''', re.VERBOSE)


logger = loggers.get('lib.club')


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


def is_discord_mutable():
    if DISCORD_MUTATIONS_ENABLED:
        logger.debug("Discord is mutable: DISCORD_MUTATIONS_ENABLED is truthy")
        return True
    logger.warning("Discord isn't mutable: DISCORD_MUTATIONS_ENABLED not set")
    return False


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


def get_roles(member_or_user):
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]


def is_message_older_than(message, date):
    if message:
        created_dt = message.created_at
        print(f"Message is from {created_dt}")
        if created_dt.date() > date:
            print(f"Message is within period: {created_dt.date()} (last reminder) > {date}")
            return False
        else:
            print(f"Message is long time ago: {created_dt.date()} (last reminder) <= {date}")
            return True
    logger.info('No message!')
    return True


def is_message_over_period_ago(message, period, today=None):
    today = today or date.today()
    ago = today - period
    print(f'{today} - {period!r} = {ago}')
    return is_message_older_than(message, ago)


def is_message_over_week_ago(message, today=None):
    return is_message_over_period_ago(message, timedelta(weeks=1), today)


def is_message_over_month_ago(message, today=None):
    return is_message_over_period_ago(message, timedelta(days=30), today)


def parse_coupon(coupon):
    match = COUPON_RE.match(coupon)
    if match:
        parts = match.groupdict()
        parts['coupon_base'] = ''.join([
            parts['coupon_name'],
            parts['coupon_suffix'],
        ])
        parts['student'] = bool(parts.pop('student_prefix'))
        return {key: value for key, value in parts.items() if value is not None}
    return {'coupon_name': coupon, 'coupon_base': coupon, 'student': False}
