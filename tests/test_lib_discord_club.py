from collections import namedtuple
from datetime import date, datetime, timedelta

import pytest

from juniorguru.lib import discord_club


StubEmoji = namedtuple('Emoji', ['name'])

StubUser = namedtuple('User', ['id'])

StubMember = namedtuple('Member', ['id', 'roles'],
                        defaults=dict(roles=[]))

StubRole = namedtuple('Role', ['id'])

StubMessage = namedtuple('Message', ['author', 'content'])

StubClubMessage = namedtuple('ClubMessage', ['created_at'])


@pytest.mark.parametrize('emoji, expected', [
    ('🆗', '🆗'),
    ('AHOJ', 'AHOJ'),
    (StubEmoji('lolpain'), 'lolpain'),
    (StubEmoji('BabyYoda'), 'babyyoda'),
    ('👋🏻', '👋'),
])
def test_emoji_name(emoji, expected):
    assert discord_club.emoji_name(emoji) == expected


@pytest.mark.parametrize('member_or_user, expected', [
    (StubUser(1), []),
    (StubMember(1, [StubRole(42), StubRole(38)]), [42, 38]),
])
def test_get_roles(member_or_user, expected):
    assert discord_club.get_roles(member_or_user) == expected


@pytest.mark.parametrize('date_, expected', [
    (date(2022, 1, 24), False),
    (date(2022, 1, 25), True),
    (date(2022, 1, 26), True),
])
def test_is_message_older_than(date_, expected):
    created_at = datetime.utcnow().replace(2022, 1, 25)
    message = StubClubMessage(created_at)

    assert discord_club.is_message_older_than(message, date_) is expected


def test_is_message_older_than_no_message():
    assert discord_club.is_message_older_than(None, date(2022, 1, 25)) is True


@pytest.mark.parametrize('today, expected', [
    (date(2022, 1, 24), False),
    (date(2022, 1, 25), True),
    (date(2022, 1, 26), True),
])
def test_is_message_over_period_ago(today, expected):
    created_at = datetime.utcnow().replace(2022, 1, 18)
    message = StubClubMessage(created_at)

    assert discord_club.is_message_over_period_ago(message, timedelta(weeks=1), today) is expected
