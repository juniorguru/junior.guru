import asyncio
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum, StrEnum, unique
from functools import wraps
from typing import Generator

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
                raise RuntimeError(f'Discord mutations not allowed! {route.method} {route.path}')
            return wrapper

        self.http.request = check_mutations(self.http.request)

    @property
    def club_guild(self) -> discord.Guild:
        return self.get_guild(CLUB_GUILD)


class MutatingProxy:
    prefixes = {'add_', 'create_', 'delete_', 'edit_', 'remove_',
                'delete', 'edit', 'send', 'purge'}

    def __init__(self, object, raises=False):
        self.object = object
        self.raises = raises

    def __getattr__(self, attr):
        if attr.startswith(tuple(self.prefixes)):
            return mutations.mutates('discord', raises=self.raises)(getattr(self.object, attr))
        raise NotImplementedError(attr)


@contextmanager
def mutating(*args, **kwargs):
    yield MutatingProxy(*args, **kwargs)


def emoji_name(reaction_emoji) -> str:
    try:
        return reaction_emoji.name.lower()
    except AttributeError:
        name = emoji.demojize(reaction_emoji).strip(':')
        if '_skin_tone' in name:
            # waving_hand_light_skin_tone -> waving_hand
            name = '_'.join(name.split('_')[:-3])
            return emoji.emojize(f':{name}:')
        return str(reaction_emoji)


def get_roles(member_or_user) -> list[int]:
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]


def is_message_older_than(message, date) -> bool:
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


def is_message_over_period_ago(message, period, today=None) -> bool:
    today = today or date.today()
    ago = today - period
    logger['is_message_over_period_ago'].debug(f'{today} - {period!r} = {ago}')
    return is_message_older_than(message, ago)


async def fetch_threads(channel) -> Generator[discord.Thread, None, None]:
    try:
        channel_threads = channel.threads
    except AttributeError:
        return  # channel type doesn't support threads (e.g. voice)
    for thread in channel_threads:
        yield thread
    async for thread in channel.archived_threads(limit=None):
        yield thread


def is_thread_after(thread, after=None) -> bool:
    if after:
        return (thread.created_at or DEFAULT_THREAD_CREATED_AT) >= after
    return True


async def add_members(thread, members):
    with mutating(thread) as proxy:
        await asyncio.gather(*[proxy.add_user(member) for member in members])


async def add_reactions(message, emojis, ordered=False):
    logger.debug(f"Reacting to message #{message.id} with emojis: {list(emojis)!r}")
    if not emojis:
        return
    try:
        with mutating(message) as proxy:
            if ordered:
                for emoji_ in emojis:
                    await proxy.add_reaction(emoji_)
            else:
                await asyncio.gather(*[proxy.add_reaction(emoji_) for emoji_ in emojis])
    except Forbidden as e:
        if 'maximum number of reactions reached' in str(e).lower():
            logger.warning(f"Message #{message.jump_url} reached maximum number of reactions!")
        else:
            raise e


def get_missing_reactions(reactions, emojis) -> set[str]:
    return set(emojis) - {emoji_name(reaction.emoji) for reaction in reactions if reaction.me}


def get_reaction(reactions, emoji) -> discord.Reaction:
    for reaction in reactions:
        if emoji_name(reaction.emoji) == emoji:
            return reaction
    return None


def get_parent_channel_id(channel) -> int:
    try:
        return channel.parent.id
    except AttributeError:
        return channel.id


def is_member(user) -> bool:
    return bool(getattr(user, 'joined_at', False))


def get_channel_name(channel: discord.abc.GuildChannel | discord.DMChannel) -> str:
    try:
        return channel.name
    except AttributeError:
        return channel.recipient.display_name
