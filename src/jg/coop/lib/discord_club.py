import asyncio
import itertools
import re
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum, StrEnum, unique
from functools import wraps
from typing import TYPE_CHECKING, AsyncGenerator, TypedDict

import discord
import emoji

from jg.coop.lib import loggers, mutations


if TYPE_CHECKING:
    from jg.coop.models.club import ClubMessage


CLUB_GUILD_ID = 769966886598737931

DEFAULT_AUTO_ARCHIVE_DURATION = 10_080  # minutes

DEFAULT_THREAD_CREATED_AT = datetime(
    2022, 1, 9, tzinfo=timezone.utc
)  # threads have 'created_at' since 2022-01-09

DEFAULT_CHANNELS_HISTORY_SINCE = timedelta(days=380)

DISCORD_LINK_RE = re.compile(
    r"""
        https://discord.com/channels/
        (
            (?P<guild_id>\d+)
            |
            (@\w+)
        )/
        (?P<channel_id>\d+)
        (/(?P<message_id>\d+))?
        /?
    """,
    re.VERBOSE,
)

REFERENCE_RE = re.compile(
    r"""
        <
            (?P<prefix>[#@&]+)
            (?P<value>[^>]+)
        >
    """,
    re.VERBOSE,
)

EMOJI_RE = re.compile(r"<a?:([^:]+):\d+>")

PINNED_MESSAGE_URL_RE = re.compile(
    r"""
        \[
            (Hop\s+na|Celý)\s+příspěvek
        \]
        \(
            (?P<url>
                https://discord.com/
                ([^\)]+)
            )
        \)
    """,
    re.VERBOSE,
)


logger = loggers.from_path(__file__)


@unique
class ClubMemberID(IntEnum):
    BOT = 797097976571887687
    DANIEL = 652142810291765248
    HONZA = 668226181769986078
    HONZA_TEST = 836610287057502208
    PAVLINA = 765643258931314728
    MILEK = 866239781313708045
    LUCIE = 1002301544496119838
    PATRIK = 625425066427154432


@unique
class ClubChannelID(IntEnum):
    ADVENTOFCODE = 1168858202415304724
    AI = 1401948283361955940
    ANNOUNCEMENTS = 789046675247333397
    BLOG = 1075091413454303272
    BOT = 1301563968883527730
    BOT_FORUM = 1205477820474593290
    BUSINESS = 1135903241792651365
    CHAT = 769966887055392768
    CLUBHOUSE = 769966887055392769
    CREATIONS = 1123525345635733504
    CV_GITHUB_LINKEDIN = 1123527619716055040
    DIARIES = 1075087192101244928
    EVENTS = 1075814161138860135
    FUN = 797040163325870092
    FUN_TOPICS = 1075038606881730570
    GROUPS = 1075087563645263922
    GUIDE_DASHBOARD = 788822884948770846
    GUIDE_EVENTS = 1169636415387205632
    GUIDE_ROLES = 1174338887406075954
    GUIDE_SPONSORS = 1177200287107264554
    INTERVIEWS = 789107031939481641
    INTRO = 788823881024405544
    JOBS = 1080052057752477716
    JOBS_TRASH = 1269384915384926259
    MENTAL_HEALTH = 864434067968360459
    MENTORING = 1240990415533113354
    META = 806215364379148348
    MODERATION = 1062730750648135680
    NEWCOMERS = 1159474100226510888
    PROMO = 1187770159595794472
    QA = 1067439203983568986
    TIL = 806621830383271937
    TIPS = 1158695711865577533
    VENTING = 815906954534191117
    WEEKLY_PLANS = 1123554774147670046


class ClubEmoji(StrEnum):
    PIN = "📌"
    SPONSOR_INTRO = "👋"


def _check_mutations(request):
    @wraps(request)
    async def wrapper(route, *args, **kwargs):
        if mutations.is_allowed("discord") or route.method in (
            "GET",
            "HEAD",
            "OPTIONS",
        ):
            return await request(route, *args, **kwargs)
        raise mutations.MutationsNotAllowedError(
            f"Discord mutations not allowed! {route.method} {route.path}"
        )

    return wrapper


class ClubClient(discord.Client):
    def __init__(self, *args, **kwargs):
        club_intents = discord.Intents(guilds=True, members=True, message_content=True)
        kwargs["intents"] = kwargs.pop("intents", club_intents)
        super().__init__(*args, **kwargs)
        self.http.request = _check_mutations(self.http.request)

    @property
    def club_guild(self) -> discord.Guild:
        return self.get_guild(CLUB_GUILD_ID)


def emoji_name(reaction_emoji: discord.GuildEmoji | discord.PartialEmoji | str) -> str:
    try:
        return reaction_emoji.name.lower()
    except AttributeError:
        if reaction_emoji[0] == "<" and reaction_emoji[-1] == ">":
            return EMOJI_RE.sub(r"\1", reaction_emoji)
        name = emoji.demojize(reaction_emoji).strip(":")
        if "_skin_tone" in name:
            # waving_hand_light_skin_tone -> waving_hand
            name = "_".join(name.split("_")[:-3])
            return emoji.emojize(f":{name}:")
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
    if match := re.match(r"^<:[^:]+:\d+>", text):
        return match.group(0)
    return None


def get_user_roles(member_or_user: discord.Member | discord.User) -> list[int]:
    return [int(role.id) for role in getattr(member_or_user, "roles", [])]


def get_guild_role(guild: discord.Guild, role_id: int) -> discord.Role:
    try:
        return next(role for role in guild.roles if role.id == role_id)
    except StopIteration:
        raise ValueError(f"Role #{role_id} not found")


def is_message_older_than(message: "discord.Message | ClubMessage", date: date) -> bool:
    logger_fn = logger["is_message_older_than"]
    if message:
        created_dt = message.created_at
        logger_fn.debug(f"Message is from {created_dt}")
        if created_dt.date() > date:
            logger_fn.debug(
                f"Message is within period: {created_dt.date()} (last reminder) > {date}"
            )
            return False
        else:
            logger_fn.debug(
                f"Message is long time ago: {created_dt.date()} (last reminder) <= {date}"
            )
            return True
    logger_fn.debug("No message!")
    return True


def is_message_over_period_ago(
    message: "discord.Message | ClubMessage", period: timedelta, today: date = None
) -> bool:
    today = today or date.today()
    ago = today - period
    logger["is_message_over_period_ago"].debug(f"{today} - {period!r} = {ago}")
    return is_message_older_than(message, ago)


async def fetch_threads(
    channel: discord.abc.GuildChannel | discord.DMChannel,
) -> AsyncGenerator[discord.Thread, None]:
    try:
        channel_threads = channel.threads
    except AttributeError:
        return  # channel type doesn't support threads (e.g. voice)
    for thread in channel_threads:
        yield thread
    async for thread in channel.archived_threads(limit=None):
        yield thread


async def add_reactions(
    message: discord.Message, emojis: list[str], ordered: bool = False
):
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
        if "maximum number of reactions reached" in str(e).lower():
            logger.warning(
                f"Message #{message.jump_url} reached maximum number of reactions!"
            )
        else:
            raise e


def get_missing_reactions(reactions: discord.Reaction, emojis: set[str]) -> set[str]:
    existing_emojis = {
        emoji_name(reaction.emoji) for reaction in reactions if reaction.me
    }
    return {emoji for emoji in emojis if emoji_name(emoji) not in existing_emojis}


def get_reaction(reactions, emoji) -> discord.Reaction:
    for reaction in reactions:
        if emoji_name(reaction.emoji) == emoji:
            return reaction
    return None


def get_parent_channel(
    channel: discord.abc.GuildChannel | discord.DMChannel,
) -> discord.abc.GuildChannel | discord.DMChannel:
    try:
        return channel.parent
    except AttributeError:
        return channel


def is_member(user: discord.User) -> bool:
    return bool(getattr(user, "joined_at", False))


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
            logger["users"][member.id].warning(e)
            return None
        raise


def is_message_pinning(message: discord.Message) -> bool:
    return (
        is_channel_dm(message.channel)
        and get_starting_emoji(message.content) == ClubEmoji.PIN
    )


def get_pinned_message_url(message: discord.Message) -> int:
    if is_message_pinning(message):
        embed_description = message.embeds[0].description
        if match := PINNED_MESSAGE_URL_RE.search(embed_description):
            return match.group("url")
    return None


def get_ui_urls(message: discord.Message) -> list[str]:
    button_urls = itertools.chain.from_iterable(
        [button.url for button in action_row.children]
        for action_row in message.components
    )
    embed_urls = (embed.url for embed in message.embeds)
    return sorted(filter(None, itertools.chain(button_urls, embed_urls)))


class DiscordLinkIDs(TypedDict):
    guild_id: int | None
    channel_id: int
    message_id: int | None


def parse_discord_link(url: str) -> DiscordLinkIDs:
    if match := DISCORD_LINK_RE.search(url):
        return DiscordLinkIDs(
            {
                name: int(value) if value else None
                for name, value in match.groupdict().items()
            }
        )
    raise ValueError(url)


def parse_channel_link(url: str) -> int:
    try:
        ids = parse_discord_link(url)
    except KeyError:
        raise ValueError(f"Invalid Discord channel URL: {url}")
    if ids["guild_id"] != CLUB_GUILD_ID:
        raise ValueError(f"Channel URL not for the club guild: {url}")
    return ids["channel_id"]


def parse_channel(channel: str) -> int:
    try:
        return int(channel)
    except ValueError:
        return int(getattr(ClubChannelID, channel.upper()))


def resolve_references(markdown: str, roles: dict[str, int] | None = None) -> str:
    markdown = re.sub(r"\n+## ", "\n## ", markdown)
    roles = {slug.upper(): id for slug, id in (roles or {}).items()}

    resolvers = {
        "@&": lambda value: roles[value],
        "@": lambda value: ClubMemberID[value],
        "#": parse_channel,
    }

    def resolve_reference(match: re.Match) -> str:
        prefix = match.group("prefix")
        value = match.group("value")
        try:
            return f"<{prefix}{resolvers[prefix](value)}>"
        except Exception as e:
            raise ValueError(f"Could not parse reference: {prefix}{value!r}") from e

    return REFERENCE_RE.sub(resolve_reference, markdown)


def is_forum_guide(message: discord.Message) -> bool:
    if message.id != message.channel.id:
        return False
    if message.channel.is_pinned():
        return True
    return False
