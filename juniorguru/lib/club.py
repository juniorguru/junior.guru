import re
import os
import importlib
import asyncio
from datetime import timedelta, date
from multiprocessing import Process

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


logger = loggers.get(__name__)


class BaseClient(discord.Client):
    @property
    def juniorguru_guild(self):
        return self.get_guild(JUNIORGURU_GUILD)


def run_discord_task(import_path):
    """
    Run given async function in a separate process.

    Separate process is used so that it's possible to run multiple one-time
    async tasks independently on each other, in separate async loops.
    """
    logger.debug(f'Running async code in a separate process: {import_path}')
    process = Process(target=_discord_task, args=[import_path])
    process.start()
    process.join()


def _discord_task(import_path):
    logger_dt = logger.getChild('discord_task')

    import_path_parts = import_path.split('.')
    module = importlib.import_module('.'.join(import_path_parts[:-1]))
    task_fn = getattr(module, import_path_parts[-1])
    logger_dt.debug(f'Imported {task_fn.__qualname__} from {task_fn.__module__}')

    if not asyncio.iscoroutinefunction(task_fn):
        raise TypeError(f"Not async function: {task_fn.__qualname__} from {task_fn.__module__}")

    class Client(BaseClient):
        async def on_ready(self):
            await self.wait_until_ready()
            logger_dt.debug('Discord connection ready')
            await task_fn(self)
            logger_dt.debug('Closing Discord client')
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            logger_dt.debug('Got an error, raising')
            raise

    intents = discord.Intents(guilds=True, members=True)
    client = Client(intents=intents)

    exc = None
    def exc_handler(loop, context):
        nonlocal exc
        logger_dt.debug('Recording exception')
        exc = context.get('exception')
        loop.default_exception_handler(context)
        logger_dt.debug('Stopping async execution')
        loop.stop()

    client.loop.set_exception_handler(exc_handler)
    logger_dt.debug('Starting')
    client.run(DISCORD_API_KEY)

    if exc:
        logger_dt.debug('Found exception, raising')
        raise exc


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
