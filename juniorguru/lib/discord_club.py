import asyncio
import re
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum, StrEnum, unique
from functools import wraps
from typing import Generator, TYPE_CHECKING

import discord
import emoji

from juniorguru.lib import loggers, mutations


if TYPE_CHECKING:
    from juniorguru.models.club import ClubMessage


CLUB_GUILD = 769966886598737931

DEFAULT_THREAD_CREATED_AT = datetime(2022, 1, 9, tzinfo=timezone.utc)  # threads have 'created_at' since 2022-01-09

DEFAULT_CHANNELS_HISTORY_SINCE = timedelta(days=380)

MESSAGE_URL_RE = re.compile(r'''
    https://discord.com/channels/
    (
        (?P<guild_id>\d+)
        |
        (@\w+)
    )/
    (?P<channel_id>\d+)/
    (?P<message_id>\d+)/?
''', re.VERBOSE)

PINNED_MESSAGE_URL_RE = re.compile(r'''
    \[
        (Hop\s+na|Celý)\s+příspěvek
    \]
    \(
        (?P<url>
            https://discord.com/
            ([^\)]+)
        )
    \)
''', re.VERBOSE)


logger = loggers.from_path(__file__)


@unique
class ClubMemberID(IntEnum):
    BOT = 797097976571887687
    HONZA = 668226181769986078
    DANIEL = 652142810291765248
    PAVLINA = 765643258931314728


@unique
class ClubChannelID(IntEnum):
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


def _check_mutations(request):
    @wraps(request)
    async def wrapper(route, *args, **kwargs):
        if (
            mutations.is_allowed('discord')
            or route.method in ('GET', 'HEAD', 'OPTIONS')
        ):
            return await request(route, *args, **kwargs)
        raise mutations.MutationsNotAllowedError(f'Discord mutations not allowed! {route.method} {route.path}')
    return wrapper


class ClubClient(discord.Client):
    def __init__(self, *args, **kwargs):
        club_intents = discord.Intents(guilds=True,
                                       members=True,
                                       message_content=True)
        kwargs['intents'] = kwargs.pop('intents', club_intents)
        super().__init__(*args, **kwargs)
        self.http.request = _check_mutations(self.http.request)

    @property
    def club_guild(self) -> discord.Guild:
        return self.get_guild(CLUB_GUILD)


def emoji_name(reaction_emoji: discord.Emoji | discord.PartialEmoji) -> str:
    try:
        return reaction_emoji.name.lower()
    except AttributeError:
        name = emoji.demojize(reaction_emoji).strip(':')
        if '_skin_tone' in name:
            # waving_hand_light_skin_tone -> waving_hand
            name = '_'.join(name.split('_')[:-3])
            return emoji.emojize(f':{name}:')
        return str(reaction_emoji)


def get_starting_emoji(text: str) -> str | None:
    text = text.lstrip()
    try:
        first_char = text[0]
    except IndexError:
        return None
    if emoji.is_emoji(first_char):
        prefix = text.split(maxsplit=1)[0]
        if emoji.is_emoji(prefix):
            return prefix
        return first_char
    if match := re.match(r'^<:[^:]+:\d+>', text):
        return match.group(0)
    return None


def get_user_roles(member_or_user: discord.Member | discord.User) -> list[int]:
    return [int(role.id) for role in getattr(member_or_user, 'roles', [])]


def get_guild_role(guild: discord.Guild, role_id: int) -> discord.Role:
    try:
        return next(role for role in guild.roles if role.id == role_id)
    except StopIteration:
        raise ValueError(f"Role #{role_id} not found")


def is_message_older_than(message: 'discord.Message | ClubMessage', date: date) -> bool:
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


def is_message_over_period_ago(message: 'discord.Message | ClubMessage', period: timedelta, today: date=None) -> bool:
    today = today or date.today()
    ago = today - period
    logger['is_message_over_period_ago'].debug(f'{today} - {period!r} = {ago}')
    return is_message_older_than(message, ago)


async def fetch_threads(channel: discord.abc.GuildChannel | discord.DMChannel) -> Generator[discord.Thread, None, None]:
    try:
        channel_threads = channel.threads
    except AttributeError:
        return  # channel type doesn't support threads (e.g. voice)
    for thread in channel_threads:
        yield thread
    async for thread in channel.archived_threads(limit=None):
        yield thread


def is_thread_after(thread: discord.Thread, after: date=None) -> bool:
    if after:
        return (thread.created_at or DEFAULT_THREAD_CREATED_AT) >= after
    return True


async def add_reactions(message: discord.Message, emojis: list[str], ordered: bool=False):
    logger.debug(f"Reacting to message #{message.id} with emojis: {list(emojis)!r}")
    if not emojis:
        return
    try:
        with mutations.mutating_discord(message) as proxy:
            if ordered:
                for emoji_ in emojis:
                    await proxy.add_reaction(emoji_)
            else:
                await asyncio.gather(*[proxy.add_reaction(emoji_) for emoji_ in emojis])
    except discord.errors.Forbidden as e:
        if 'maximum number of reactions reached' in str(e).lower():
            logger.warning(f"Message #{message.jump_url} reached maximum number of reactions!")
        else:
            raise e


def get_missing_reactions(reactions: discord.Reaction, emojis: set[str]) -> set[str]:
    return set(emojis) - {emoji_name(reaction.emoji) for reaction in reactions if reaction.me}


def get_reaction(reactions, emoji) -> discord.Reaction:
    for reaction in reactions:
        if emoji_name(reaction.emoji) == emoji:
            return reaction
    return None


def get_parent_channel_id(channel: discord.abc.GuildChannel | discord.DMChannel) -> int:
    try:
        return channel.parent.id
    except AttributeError:
        return channel.id


def is_member(user: discord.User) -> bool:
    return bool(getattr(user, 'joined_at', False))


def get_channel_name(channel: discord.abc.GuildChannel | discord.DMChannel) -> str:
    try:
        return channel.name
    except AttributeError:
        return channel.recipient.display_name


def is_channel_dm(channel: discord.abc.GuildChannel | discord.DMChannel) -> bool:
    return channel.type == discord.ChannelType.private


def is_channel_private(channel: discord.abc.GuildChannel | discord.DMChannel) -> bool:
    if is_channel_dm(channel):
        return True
    assert channel.guild.default_role
    return not channel.permissions_for(channel.guild.default_role).read_messages


async def get_or_create_dm_channel(member: discord.Member) -> None | discord.DMChannel:
    if member.dm_channel:
        return member.dm_channel
    try:
        with mutations.allowing_discord():
            return await member.create_dm()
    except discord.HTTPException as e:
        if e.code == 50007:  # cannot send messages to this user
            logger['users'][member.id].warning(e)
            return None
        raise


def is_message_pinning(message: discord.Message) -> bool:
    return (is_channel_dm(message.channel)
            and get_starting_emoji(message.content) == ClubEmoji.PIN)


def get_pinned_message_url(message: discord.Message) -> int:
    if is_message_pinning(message):
        embed_description = message.embeds[0].description
        if match := PINNED_MESSAGE_URL_RE.search(embed_description):
            return match.group('url')
    return None


def parse_message_url(url: str) -> int:
    if match := MESSAGE_URL_RE.search(url):
        return {name: int(value) if value else None
                for name, value in match.groupdict().items()}
    raise ValueError(url)
