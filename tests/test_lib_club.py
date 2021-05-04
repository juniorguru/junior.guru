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


@pytest.mark.parametrize('emoji, expected', [
    ('🆗', '🆗'),
    ('AHOJ', 'AHOJ'),
    (DummyEmoji('lolpain'), 'lolpain'),
    (DummyEmoji('BabyYoda'), 'babyyoda'),
])
def test_emoji_name(emoji, expected):
    assert club.emoji_name(emoji) == expected


@pytest.mark.parametrize('url, expected', [
    ('https://cdn.discordapp.com/avatars/524854651644936192/b807c46b5da690cc3365c1fc50159872.webp?size=1024', False),
    ('https://cdn.discordapp.com/embed/avatars/4.png', True),
])
def test_is_default_avatar(url, expected):
    assert club.is_default_avatar(url) is expected


def test_is_default_avatar_handles_non_string():
    class NonString:
        def __init__(self, url):
            self.url = url

        def __str__(self):
            return self.url

    assert club.is_default_avatar(NonString('https://cdn.discordapp.com/embed/avatars/4.png')) is True


DummyUser = namedtuple('User', ['id'])
DummyMember = namedtuple('Member', ['id', 'roles'])
DummyRole = namedtuple('Role', ['id'])


@pytest.mark.parametrize('member_or_user, expected', [
    (DummyUser(1), []),
    (DummyMember(1, [DummyRole(42), DummyRole(38)]), [42, 38]),
])
def test_get_roles(member_or_user, expected):
    assert club.get_roles(member_or_user) == expected
