import asyncio
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum, StrEnum, unique
from functools import wraps

import discord
import emoji
from discord.errors import Forbidden

from juniorguru.lib import loggers
from juniorguru.lib.mutations import mutations


CLUB_GUILD = 769966886598737931

DEFAULT_THREAD_CREATED_AT = datetime(2022, 1, 9, tzinfo=timezone.utc)  # threads have 'created_at' since 2022-01-09

DEFAULT_CHANNELS_HISTORY_SINCE = timedelta(days=380)


logger = loggers.from_path(__file__)


@unique
class ClubMember(IntEnum):
    BOT = 797097976571887687
    HONZA = 668226181769986078
    DANIEL = 652142810291765248
    PAVLINA = 765643258931314728


@unique
class ClubChannel(IntEnum):
    INTRO = 788823881024405544
    ANNOUNCEMENTS = 789046675247333397
    BOT = 797107515186741248
    JOBS = 1080052057752477716
    CV_FEEDBACK = 839059491432431616
    EVENTS = 1075814161138860135
    MENTORING = 976054742117658634
    INTERVIEWS = 789107031939481641
    DASHBOARD = 788822884948770846
    FUN = 797040163325870092
    FUN_TOPICS = 1075038606881730570


class ClubEmoji(StrEnum):
    PIN = '📌'
    PARTNER_INTRO = '👋'


class ClubClient(discord.Client):
    def __init__(self, *args, **kwargs):
        club_intents = discord.Intents(guilds=True,
                                       members=True,
                                       message_content=True)
        kwargs['intents'] = kwargs.pop('intents', club_intents)

        super().__init__(*args, **kwargs)

        def check_mutations(request):
            @wraps(request)
            async def wrapper(route, *args, **kwargs):
                if (
                    mutations.is_allowed('discord')
                    or route.method in ('GET', 'HEAD', 'OPTIONS')
                ):
                    return await request(route, *args, **kwargs)
                logger.error(f'Discord mutations not allowed! {route.method} {route.path}')
                raise RuntimeError('Discord mutations not allowed!')
            return wrapper

        self.http.request = check_mutations(self.http.request)

    @property
    def club_guild(self) -> discord.Guild:
        return self.get_guild(CLUB_GUILD)


class MutatingProxy:
    reading = {'fetch_', 'get_', 'is_'}
    writing = {'add_', 'create_', 'delete_', 'edit_', 'remove_',
               'delete', 'edit', 'send', 'purge'}

    def __init__(self, object):
        self.object = object

    def __getattr__(self, attr):
        if attr.startswith(tuple(self.reading)):
            return getattr(self.object, attr)
        if attr.startswith(tuple(self.writing)):
            return mutations.mutation('discord', getattr(self.object, attr))
        raise NotImplementedError(f"Not sure what to do with attribute {attr!r}")


@contextmanager
def mutating(object):
    yield MutatingProxy(object)


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


async def fetch_messages(channel, after=None):
    try:
        channel_history = channel.history
    except AttributeError:
        pass  # channel type doesn't support history (e.g. forum)
    else:
        async for message in channel_history(limit=None, after=after):
            yield message


async def fetch_threads(channel):
    try:
        channel_threads = channel.threads
    except AttributeError:
        return  # channel type doesn't support threads (e.g. voice)
    for thread in channel_threads:
        yield thread
    async for thread in channel.archived_threads(limit=None):
        yield thread


def is_thread_after(thread, after=None):
    if after:
        return (thread.created_at or DEFAULT_THREAD_CREATED_AT) >= after
    return thread


@mutations.mutates('discord')
async def add_members(thread, members):
    await asyncio.gather(*[thread.add_user(member) for member in members])


@mutations.mutates('discord')
async def add_reactions(message, emojis, ordered=False):
    logger.debug(f"Reacting to message #{message.id} with emojis: {list(emojis)!r}")
    if not emojis:
        return
    try:
        if ordered:
            for emoji_ in emojis:
                await message.add_reaction(emoji_)
        else:
            await asyncio.gather(*[message.add_reaction(emoji_) for emoji_ in emojis])
    except Forbidden as e:
        if 'maximum number of reactions reached' in str(e).lower():
            logger.warning(f"Message #{message.jump_url} reached maximum number of reactions!")
        else:
            raise e


def get_missing_reactions(reactions, emojis):
    return set(emojis) - {emoji_name(reaction.emoji) for reaction in reactions if reaction.me}


def get_reaction(reactions, emoji):
    for reaction in reactions:
        if emoji_name(reaction.emoji) == emoji:
            return reaction
    return None
