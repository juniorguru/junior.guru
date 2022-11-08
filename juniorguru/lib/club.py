import asyncio
import importlib
import os
import re
from datetime import date
from multiprocessing import Process

import discord
import emoji

from juniorguru.lib import loggers


DISCORD_MUTATIONS_ENABLED = bool(int(os.getenv('DISCORD_MUTATIONS_ENABLED', 0)))

DISCORD_API_KEY = os.getenv('DISCORD_API_KEY') or None

JUNIORGURU_GUILD = 769966886598737931

EMOJI_PIN = '📌'

EMOJI_UPVOTES = ['👍', '❤️', '😍', '🥰', '💕', '♥️', '💖', '💙', '💗', '💜', '💞', '💓', '💛', '🖤', '💚', '😻', '🧡', '👀',
                 '💯', '🤩', '😋', '💟', '🤍', '🤎', '💡', '👆', '👏', '🥇', '🏆', '✔️', 'plus_one', '👌', 'babyyoda', 'meowsheart',
                 'meowthumbsup', '✅', '🤘', 'this', 'dk', '🙇‍♂️', '🙇', '🙇‍♀️', 'kgsnice', 'successkid', 'white_check_mark',
                 'notbad', 'updoot', '🆒', '🔥', 'yayfrog', 'partyparrot', 'drakeyes', 'awyeah', 'meowparty', EMOJI_PIN]

EMOJI_DOWNVOTES = ['👎']

JUNIORGURU_BOT = 797097976571887687

HONZAJAVOREK = 668226181769986078

MODERATORS_ROLE = 795609174385098762

INTRO_CHANNEL = 788823881024405544  # ahoj

ANNOUNCEMENTS_CHANNEL = 789046675247333397  # oznámení

FUN_CHANNEL = 797040163325870092  # volná-zábava

BOT_CHANNEL = 797107515186741248  # roboti

JOBS_CHANNEL = 834443926655598592  # práce-bot

MENTORING_CHANNEL = 976054742117658634  # mentoring

UPVOTES_EXCLUDE_CHANNELS = [
    INTRO_CHANNEL,
    ANNOUNCEMENTS_CHANNEL,
    BOT_CHANNEL,
    FUN_CHANNEL,
    788822884948770846,  # pravidla
    788822884948770847,  # moderátoři
]

TOP_MEMBERS_PERCENT = 0.05

RECENT_PERIOD_DAYS = 30

IS_NEW_PERIOD_DAYS = 15

COUPON_RE = re.compile(r'''
    ^
        (?P<name>
            (?P<student_prefix>STUDENT)?
            [A-Z0-9]+
            [A-Z]+
        )
        (?P<suffix>[0-9]{5,})
    $
''', re.VERBOSE)


logger = loggers.from_path(__file__)


class BaseClient(discord.Client):
    @property
    def juniorguru_guild(self):
        return self.get_guild(JUNIORGURU_GUILD)


def run_discord_task(import_path, *args):
    """
    Run given async function in a separate process.

    Separate process is used so that it's possible to run multiple one-time
    async tasks independently on each other, in separate async loops.
    """
    logger.debug(f'Running async code in a separate process: {import_path}')
    process = Process(target=_discord_task, args=[import_path, args])
    process.start()
    process.join()
    if process.exitcode != 0:
        raise RuntimeError(f'Process for running async code finished with non-zero exit code: {process.exitcode}')


def _discord_task(import_path, args):
    logger_dt = logger['discord_task']

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
            await task_fn(self, *args)
            logger_dt.debug('Closing Discord client')
            await self.close()

        async def on_error(self, event, *args, **kwargs):
            logger_dt.debug('Got an error, raising')
            raise

    intents = discord.Intents(guilds=True, members=True, message_content=True)
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


def count_upvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_UPVOTES])


def count_downvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_DOWNVOTES])


def emoji_name(reaction_emoji):
    try:
        return reaction_emoji.name.lower()
    except AttributeError:
        name = emoji.demojize(reaction_emoji).strip(':')
        if '_skin_tone' in name:
            # waving_hand_light_skin_tone -> waving_hand
            name = '_'.join(name.split('_')[:-3])
            return emoji.emojize(f':{name}:')
        return str(reaction_emoji)


def get_roles(member_or_user):
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]


def is_message_older_than(message, date):
    logger_fn = logger['is_message_older_than']
    if message:
        created_dt = message.created_at
        logger_fn.debug(f"Message is from {created_dt}")
        if created_dt.date() > date:
            logger_fn.debug(f"Message is within period: {created_dt.date()} (last reminder) > {date}")
            return False
        else:
            logger_fn.debug(f"Message is long time ago: {created_dt.date()} (last reminder) <= {date}")
            return True
    logger_fn.debug('No message!')
    return True


def is_message_over_period_ago(message, period, today=None):
    today = today or date.today()
    ago = today - period
    logger['is_message_over_period_ago'].debug(f'{today} - {period!r} = {ago}')
    return is_message_older_than(message, ago)


def parse_coupon(coupon):
    match = COUPON_RE.match(coupon)
    if match:
        parts = match.groupdict()
        parts['coupon'] = ''.join([
            parts['name'],
            parts['suffix'],
        ])
        parts['is_student'] = bool(parts.pop('student_prefix'))
        return {key: value for key, value in parts.items() if value is not None}
    return {'name': coupon, 'coupon': coupon, 'is_student': False}


def is_message_bot_reminder(message):
    return (message.author.id == JUNIORGURU_BOT and
            message.content and
            emoji.is_emoji(message.content[0]))
