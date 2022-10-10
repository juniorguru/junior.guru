from collections import namedtuple
from datetime import date, datetime, timedelta

import pytest

from juniorguru.lib import club


StubReaction = namedtuple('Reaction', ['emoji', 'count'])

StubEmoji = namedtuple('Emoji', ['name'])

StubUser = namedtuple('User', ['id'])

StubMember = namedtuple('Member', ['id', 'roles'],
                        defaults=dict(roles=[]))

StubRole = namedtuple('Role', ['id'])

StubMessage = namedtuple('Message', ['author', 'content'])

StubClubMessage = namedtuple('ClubMessage', ['created_at'])


def test_count_upvotes():
    reactions = [StubReaction(StubEmoji('plus_one'), 4), StubReaction('👍', 1), StubReaction('🐣', 3)]
    assert club.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [StubReaction('🙁', 4), StubReaction('👎', 1), StubReaction('🐣', 3)]
    assert club.count_downvotes(reactions) == 1


@pytest.mark.parametrize('emoji, expected', [
    ('🆗', '🆗'),
    ('AHOJ', 'AHOJ'),
    (StubEmoji('lolpain'), 'lolpain'),
    (StubEmoji('BabyYoda'), 'babyyoda'),
])
def test_emoji_name(emoji, expected):
    assert club.emoji_name(emoji) == expected


@pytest.mark.parametrize('member_or_user, expected', [
    (StubUser(1), []),
    (StubMember(1, [StubRole(42), StubRole(38)]), [42, 38]),
])
def test_get_roles(member_or_user, expected):
    assert club.get_roles(member_or_user) == expected


@pytest.mark.parametrize('message, expected', [
    (StubMessage(StubMember(123), 'Hello!'), False),
    (StubMessage(StubMember(123), '💡 Hello!'), False),
    (StubMessage(StubMember(club.JUNIORGURU_BOT), 'Hello!'), False),
    (StubMessage(StubMember(club.JUNIORGURU_BOT), '💡 Hello!'), True),
])
def test_is_message_bot_reminder(message, expected):
    assert club.is_message_bot_reminder(message) is expected


@pytest.mark.parametrize('date_, expected', [
    (date(2022, 1, 24), False),
    (date(2022, 1, 25), True),
    (date(2022, 1, 26), True),
])
def test_is_message_older_than(date_, expected):
    created_at = datetime.utcnow().replace(2022, 1, 25)
    message = StubClubMessage(created_at)

    assert club.is_message_older_than(message, date_) is expected


def test_is_message_older_than_no_message():
    assert club.is_message_older_than(None, date(2022, 1, 25)) is True


@pytest.mark.parametrize('today, expected', [
    (date(2022, 1, 24), False),
    (date(2022, 1, 25), True),
    (date(2022, 1, 26), True),
])
def test_is_message_over_period_ago(today, expected):
    created_at = datetime.utcnow().replace(2022, 1, 18)
    message = StubClubMessage(created_at)

    assert club.is_message_over_period_ago(message, timedelta(weeks=1), today) is expected


@pytest.mark.parametrize('coupon, expected', [
    ('GARGAMEL', dict(name='GARGAMEL',
                      coupon='GARGAMEL',
                      is_student=False)),
    ('FAKTUROID123456', dict(name='FAKTUROID',
                             suffix='123456',
                             coupon='FAKTUROID123456',
                             is_student=False)),
    ('CDN77COM123456', dict(name='CDN77COM',
                            suffix='123456',
                            coupon='CDN77COM123456',
                            is_student=False)),
    ('STUDENTGARGAMEL69320144', dict(name='STUDENTGARGAMEL',
                                     suffix='69320144',
                                     coupon='STUDENTGARGAMEL69320144',
                                     is_student=True)),
])
def test_parse_coupon(coupon, expected):
    assert club.parse_coupon(coupon) == expected


def test_parse_coupon_raises_on_wrong_input():
    with pytest.raises(TypeError):
        club.parse_coupon(None)
