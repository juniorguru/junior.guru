import pytest

from collections import namedtuple

from juniorguru.lib import club


DummyReaction = namedtuple('Reaction', ['emoji', 'count'])
DummyEmoji = namedtuple('Emoji', ['name'])


def test_count_upvotes():
    reactions = [DummyReaction(DummyEmoji('plus_one'), 4), DummyReaction('👍', 1), DummyReaction('🐣', 3)]
    assert club.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [DummyReaction('🙁', 4), DummyReaction('👎', 1), DummyReaction('🐣', 3)]
    assert club.count_downvotes(reactions) == 1


def test_count_pins():
    reactions = [DummyReaction(DummyEmoji('plus_one'), 4), DummyReaction('📌', 3), DummyReaction('🐣', 3)]
    assert club.count_pins(reactions) == 3


@pytest.mark.parametrize('emoji, expected', [
    ('🆗', '🆗'),
    ('AHOJ', 'AHOJ'),
    (DummyEmoji('lolpain'), 'lolpain'),
    (DummyEmoji('BabyYoda'), 'babyyoda'),
])
def test_emoji_name(emoji, expected):
    assert club.emoji_name(emoji) == expected


DummyUser = namedtuple('User', ['id'])
DummyMember = namedtuple('Member', ['id', 'roles'])
DummyRole = namedtuple('Role', ['id'])


@pytest.mark.parametrize('member_or_user, expected', [
    (DummyUser(1), []),
    (DummyMember(1, [DummyRole(42), DummyRole(38)]), [42, 38]),
])
def test_get_roles(member_or_user, expected):
    assert club.get_roles(member_or_user) == expected
