from collections import namedtuple
from datetime import date, datetime, timedelta

import pytest

from juniorguru.lib import club


StubReaction = namedtuple('Reaction', ['emoji', 'count'])
StubEmoji = namedtuple('Emoji', ['name'])


def test_count_upvotes():
    reactions = [StubReaction(StubEmoji('plus_one'), 4), StubReaction('👍', 1), StubReaction('🐣', 3)]
    assert club.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [StubReaction('🙁', 4), StubReaction('👎', 1), StubReaction('🐣', 3)]
    assert club.count_downvotes(reactions) == 1


def test_count_pins():
    reactions = [StubReaction(StubEmoji('plus_one'), 4), StubReaction('📌', 3), StubReaction('🐣', 3)]
    assert club.count_pins(reactions) == 3


@pytest.mark.parametrize('emoji, expected', [
    ('🆗', '🆗'),
    ('AHOJ', 'AHOJ'),
    (StubEmoji('lolpain'), 'lolpain'),
    (StubEmoji('BabyYoda'), 'babyyoda'),
])
def test_emoji_name(emoji, expected):
    assert club.emoji_name(emoji) == expected


StubUser = namedtuple('User', ['id'])
StubMember = namedtuple('Member', ['id', 'roles'])
StubRole = namedtuple('Role', ['id'])


@pytest.mark.parametrize('member_or_user, expected', [
    (StubUser(1), []),
    (StubMember(1, [StubRole(42), StubRole(38)]), [42, 38]),
])
def test_get_roles(member_or_user, expected):
    assert club.get_roles(member_or_user) == expected


StubClubMessage = namedtuple('ClubMessage', ['created_at'])


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
    ('GARGAMEL', dict(coupon_name='GARGAMEL',
                      coupon_base='GARGAMEL',
                      student=False)),
    ('FAKTUROID123456', dict(coupon_name='FAKTUROID',
                             coupon_suffix='123456',
                             coupon_base='FAKTUROID123456',
                             student=False)),
    ('FAKTUROID123456I12345678', dict(coupon_name='FAKTUROID',
                                      coupon_suffix='123456',
                                      coupon_base='FAKTUROID123456',
                                      invoice_id='12345678',
                                      student=False)),
    ('STUDENTGARGAMEL69320144', dict(coupon_name='STUDENTGARGAMEL',
                                     coupon_suffix='69320144',
                                     coupon_base='STUDENTGARGAMEL69320144',
                                     student=True)),
    ('STUDENTGARGAMEL69320144V2', dict(coupon_name='STUDENTGARGAMEL',
                                       coupon_suffix='69320144',
                                       coupon_base='STUDENTGARGAMEL69320144',
                                       student=True,
                                       version='2'))
])
def test_parse_coupon(coupon, expected):
    assert club.parse_coupon(coupon) == expected


def test_parse_coupon_raises_on_wrong_input():
    with pytest.raises(TypeError):
        club.parse_coupon(None)


def test_parse_coupon_raises_when_getting_empty_part():
    with pytest.raises(KeyError):
        club.parse_coupon('FAKTUROID123456')['invoice_id']
