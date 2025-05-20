from collections import namedtuple
from datetime import date, datetime, timedelta, timezone

import pytest
from discord import ChannelType, Route

from jg.coop.lib import discord_club
from jg.coop.lib.mutations import (
    MutationsNotAllowedError,
    _get_allowed,
    _set_allowed,
    allow,
)


StubEmoji = namedtuple("Emoji", ["name"])

StubUser = namedtuple("User", ["id"])

StubMember = namedtuple("Member", ["id", "roles"], defaults=[[]])

StubRole = namedtuple("Role", ["id"])

StubGuild = namedtuple("Guild", ["roles"])

StubMessage = namedtuple("Message", ["author", "content"])

StubClubMessage = namedtuple("ClubMessage", ["created_at"])


@pytest.fixture
def nothing_allowed():
    dump = _get_allowed()
    _set_allowed([])
    try:
        yield
    finally:
        _set_allowed(dump)


@pytest.mark.parametrize(
    "emoji, expected",
    [
        ("🆗", "🆗"),
        ("AHOJ", "AHOJ"),
        (StubEmoji("lolpain"), "lolpain"),
        (StubEmoji("BabyYoda"), "babyyoda"),
        ("👋🏻", "👋"),
    ],
)
def test_emoji_name(emoji, expected):
    assert discord_club.emoji_name(emoji) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        pytest.param("", None, id="empty"),
        pytest.param("😀", "😀", id="emoji"),
        pytest.param("😀 blah blah blah", "😀", id="emoji with text"),
        pytest.param(
            "👨‍👩‍👦 blah blah blah", "👨‍👩‍👦", id="multi-byte emoji with text"
        ),
        pytest.param("     😀", "😀", id="emoji with spaces"),
        pytest.param(
            "<:discordthread:993580255287705681>",
            "<:discordthread:993580255287705681>",
            id="custom emoji",
        ),
        pytest.param(
            "<:discordthread:993580255287705681> blah blah blah",
            "<:discordthread:993580255287705681>",
            id="custom emoji with text",
        ),
        pytest.param(
            "    <:discordthread:993580255287705681>",
            "<:discordthread:993580255287705681>",
            id="custom emoji with spaces",
        ),
    ],
)
def test_get_starting_emoji(text, expected):
    assert discord_club.get_starting_emoji(text) == expected


@pytest.mark.parametrize(
    "member_or_user, expected",
    [
        (StubUser(1), []),
        (StubMember(1, [StubRole(42), StubRole(38)]), [42, 38]),
    ],
)
def test_get_user_roles(member_or_user, expected):
    assert discord_club.get_user_roles(member_or_user) == expected


def test_get_guild_role():
    role42 = StubRole(42)
    role38 = StubRole(38)
    guild = StubGuild([role42, role38])

    assert discord_club.get_guild_role(guild, 42) == role42


def test_get_guild_role_not_found_raises():
    with pytest.raises(ValueError):
        discord_club.get_guild_role(StubGuild([]), 42)


@pytest.mark.parametrize(
    "date_, expected",
    [
        (date(2022, 1, 24), False),
        (date(2022, 1, 25), True),
        (date(2022, 1, 26), True),
    ],
)
def test_is_message_older_than(date_, expected):
    created_at = datetime(2022, 1, 25)
    message = StubClubMessage(created_at)

    assert discord_club.is_message_older_than(message, date_) is expected


def test_is_message_older_than_no_message():
    assert discord_club.is_message_older_than(None, date(2022, 1, 25)) is True


@pytest.mark.parametrize(
    "today, expected",
    [
        (date(2022, 1, 24), False),
        (date(2022, 1, 25), True),
        (date(2022, 1, 26), True),
    ],
)
def test_is_message_over_period_ago(today, expected):
    created_at = datetime(2022, 1, 18)
    message = StubClubMessage(created_at)

    assert (
        discord_club.is_message_over_period_ago(message, timedelta(weeks=1), today)
        is expected
    )


@pytest.mark.parametrize(
    "link_text",
    [
        "Celý příspěvek",
        "Hop na příspěvek",
    ],
)
def test_get_pinned_message_url(link_text):
    StubEmbed = namedtuple("Embed", ["description"])
    StubChannel = namedtuple("Channel", ["type"])
    StubMessage = namedtuple("Message", ["content", "embeds", "channel"])

    description = (
        "**Dan Srb** v kanálu „ITnetwork informační hodnota kurzů”:"
        "\n> Zjistit se to dá z Excelového souboru tady https://www.msmt.cz/vzdelavani/dalsi-vzdelavani/databaze a "
        "řetězec SDA se v něm vůbec nevyskytuje, takže to nevypadá, že akreditaci mají. Za loňsko byly uděleny tyto "
        "akreditace, kde je nějaké programování. ``` Číslo jednací Vzdělávací zařízení Email žadatele Pro pracovní "
        "činnost MSMT-16743/2022-6 b4u consulting s.r.o. t.kosina@consultant.com Programátor www aplikací "
        "MSMT-6316/2022-2 Edu partners s.r.o. info@edu-partners.cz Programátor www aplikací…"
        f"\n[{link_text}](https://discord.com/channels/769966886598737931/1083734944121102436/1089250472776454154)"
    )
    message = StubMessage(
        "📌 ...", [StubEmbed(description)], StubChannel(type=ChannelType.private)
    )

    assert (
        discord_club.get_pinned_message_url(message)
        == "https://discord.com/channels/769966886598737931/1083734944121102436/1089250472776454154"
    )


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://discord.com/channels/769966886598737931/1083734944121102436/1089250472776454154",
            {
                "guild_id": 769966886598737931,
                "channel_id": 1083734944121102436,
                "message_id": 1089250472776454154,
            },
        ),
        (
            "https://discord.com/channels/@me/834779122256576522/968729020357296139",
            {
                "guild_id": None,
                "channel_id": 834779122256576522,
                "message_id": 968729020357296139,
            },
        ),
        (
            "https://discord.com/channels/769966886598737931/1295314307147632692",
            {
                "guild_id": 769966886598737931,
                "channel_id": 1295314307147632692,
                "message_id": None,
            },
        ),
    ],
)
def test_parse_discord_link(url, expected):
    assert discord_club.parse_discord_link(url) == expected


@pytest.mark.parametrize(
    "method",
    [
        "GET",
        "OPTIONS",
        "HEAD",
    ],
)
@pytest.mark.asyncio
async def test_check_mutations(nothing_allowed, method):
    @discord_club._check_mutations
    async def request(*args, **kwargs):
        return args, kwargs

    route = Route(method, "/something")

    assert await request(route, 1, 2, kwarg1=3, kwarg2=4) == (
        (route, 1, 2),
        {"kwarg1": 3, "kwarg2": 4},
    )


@pytest.mark.parametrize(
    "method",
    [
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    ],
)
@pytest.mark.asyncio
async def test_check_mutations_raises(nothing_allowed, method):
    @discord_club._check_mutations
    async def request(*args, **kwargs):
        return args, kwargs

    route = Route(method, "/something")

    with pytest.raises(MutationsNotAllowedError):
        await request(route, 1, 2, kwarg1=3, kwarg2=4)


@pytest.mark.parametrize(
    "method",
    [
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
    ],
)
@pytest.mark.asyncio
async def test_check_mutations_doesnt_raise_if_discord_allowed(nothing_allowed, method):
    allow("discord")

    @discord_club._check_mutations
    async def request(*args, **kwargs):
        return args, kwargs

    route = Route(method, "/something")

    assert await request(route, 1, 2, kwarg1=3, kwarg2=4) == (
        (route, 1, 2),
        {"kwarg1": 3, "kwarg2": 4},
    )


@pytest.mark.parametrize(
    "created_at, is_pinned, after, expected",
    [
        (
            None,
            False,
            datetime(2022, 1, 8, tzinfo=timezone.utc),
            True,
        ),
        (
            None,
            False,
            datetime(2022, 1, 9, tzinfo=timezone.utc),
            True,
        ),
        (
            None,
            False,
            datetime(2022, 1, 10, tzinfo=timezone.utc),
            False,
        ),
        (
            datetime(2023, 8, 30, tzinfo=timezone.utc),
            False,
            datetime(2023, 8, 29, tzinfo=timezone.utc),
            True,
        ),
        (
            datetime(2023, 8, 30, tzinfo=timezone.utc),
            False,
            datetime(2023, 8, 30, tzinfo=timezone.utc),
            True,
        ),
        (
            datetime(2023, 8, 30, tzinfo=timezone.utc),
            False,
            datetime(2023, 8, 31, tzinfo=timezone.utc),
            False,
        ),
        (
            None,
            True,
            datetime(2022, 1, 8, tzinfo=timezone.utc),
            True,
        ),
        (
            None,
            True,
            datetime(2022, 1, 10, tzinfo=timezone.utc),
            True,
        ),
        (
            datetime(2023, 8, 30, tzinfo=timezone.utc),
            True,
            datetime(2023, 8, 31, tzinfo=timezone.utc),
            True,
        ),
    ],
)
def test_is_thread_after_default(created_at, is_pinned, after, expected):
    StubThread = namedtuple("Thread", ["created_at", "is_pinned"])
    thread = StubThread(created_at, lambda: is_pinned)

    assert discord_club.is_thread_after(thread, after) is expected


def test_get_missing_reactions():
    StubReaction = namedtuple("Reaction", ["emoji", "me"])
    reactions = [StubReaction("👍", True), StubReaction("👎", True)]

    assert discord_club.get_missing_reactions(reactions, ["👍", "👎", "🤷"]) == {"🤷"}


def test_get_missing_reactions_excludes_emojis_from_others():
    StubReaction = namedtuple("Reaction", ["emoji", "me"])
    reactions = [StubReaction("👍", False), StubReaction("👎", True)]

    assert discord_club.get_missing_reactions(reactions, ["👍", "👎", "🤷"]) == {
        "👍",
        "🤷",
    }


def test_get_reaction():
    StubReaction = namedtuple("Reaction", ["emoji"])
    reaction_up = StubReaction("👍")
    reaction_down = StubReaction("👎")

    assert discord_club.get_reaction([reaction_up, reaction_down], "👍") == reaction_up


def test_get_parent_channel():
    StubChannel = namedtuple("Channel", ["id"])
    channel = StubChannel(1)

    assert discord_club.get_parent_channel(channel).id == 1


def test_get_parent_channel_thread():
    StubChannel = namedtuple("Channel", ["id", "parent"])
    channel = StubChannel(1, None)
    thread = StubChannel(2, channel)

    assert discord_club.get_parent_channel(thread).id == 1


def test_is_member_user():
    StubUser = namedtuple("User", ["id"])
    user = StubUser(1)

    assert discord_club.is_member(user) is False


def test_is_member_member():
    StubMember = namedtuple("Member", ["id", "joined_at"])
    member = StubMember(1, datetime(2021, 1, 1, tzinfo=timezone.utc))

    assert discord_club.is_member(member) is True


def test_get_channel_name_guild():
    StubChannel = namedtuple("Channel", ["name"])
    channel = StubChannel("ahoj")

    assert discord_club.get_channel_name(channel) == "ahoj"


def test_get_channel_name_dm():
    StubUser = namedtuple("User", ["display_name"])
    user = StubUser("Gargamel")
    StubDMChannel = namedtuple("DMChannel", ["recipient"])
    channel = StubDMChannel(user)

    assert discord_club.get_channel_name(channel) == "Gargamel"


@pytest.mark.parametrize(
    "channel, expected",
    [
        ("789046675247333397", 789046675247333397),
        ("ANNOUNCEMENTS", 789046675247333397),
        ("announcements", 789046675247333397),
    ],
)
def test_parse_channel(channel, expected):
    assert discord_club.parse_channel(channel) == expected
