import pytest

from collections import namedtuple

from juniorguru.lib import club


@pytest.mark.parametrize('value,expected', [
    (123, 123),
    ('roboti', 797107515186741248),
    ('xyz-doesnt-exist', 'xyz-doesnt-exist'),
])
def test_translate_channel_id(value, expected):
    assert club.translate_channel_id(value) == expected


DummyReaction = namedtuple('Reaction', ['emoji', 'count'])


def test_count_upvotes():
    reactions = [DummyReaction('❤️', 4), DummyReaction('👍', 1), DummyReaction('🐣', 4)]
    assert club.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [DummyReaction('🙁', 4), DummyReaction('👎', 1), DummyReaction('🐣', 4)]
    assert club.count_downvotes(reactions) == 5


DummyChannel = namedtuple('Channel', ['name', 'category'], defaults=[None])
DummyCategory = namedtuple('Category', ['name'])


def test_exclude_categories_defaults():
    assert list(club.exclude_categories([
        DummyChannel('channel-without-category'),
        DummyChannel('channel-with-category', DummyCategory('category')),
        DummyChannel('channel-inside-coreskill1', DummyCategory('🟨 coreskill 🟨')),
        DummyChannel('channel-inside-coreskill2', DummyCategory('coreskill')),
    ])) == [
        DummyChannel('channel-without-category'),
        DummyChannel('channel-with-category', DummyCategory('category')),
    ]


def test_exclude_categories_explicit():
    assert list(club.exclude_categories([
        DummyChannel('channel-without-category'),
        DummyChannel('channel-with-category-moo', DummyCategory('moo')),
        DummyChannel('channel-with-category-foo', DummyCategory('foo')),
        DummyChannel('channel-with-category-bar', DummyCategory('bar')),
        DummyChannel('channel-inside-coreskill1', DummyCategory('🟨 coreskill 🟨')),
        DummyChannel('channel-inside-coreskill2', DummyCategory('coreskill')),
    ], [r'\bfo*\b', r'bar'])) == [
        DummyChannel('channel-without-category'),
        DummyChannel('channel-with-category-moo', DummyCategory('moo')),
        DummyChannel('channel-inside-coreskill1', DummyCategory('🟨 coreskill 🟨')),
        DummyChannel('channel-inside-coreskill2', DummyCategory('coreskill')),
    ]


def test_exclude_channels_defaults():
    assert list(club.exclude_channels([
        DummyChannel('foo'),
        DummyChannel('moo'),
        DummyChannel('roboti'),
    ])) == [
        DummyChannel('foo'),
        DummyChannel('moo'),
    ]


def test_exclude_channels_explicit():
    assert list(club.exclude_channels([
        DummyChannel('foo'),
        DummyChannel('moo'),
        DummyChannel('bar'),
        DummyChannel('roboti'),
    ], [r'\b\wo*\b', r'gargamel'])) == [
        DummyChannel('bar'),
        DummyChannel('roboti'),
    ]


DummyUser = namedtuple('User', ['id', 'bot'], defaults=[False])


def test_exclude_bots():
    assert list(club.exclude_bots([
        DummyUser(1, True),
        DummyUser(2),
        DummyUser(3, True),
    ])) == [
        DummyUser(2),
    ]


def test_exclude_members_defaults():
    assert list(club.exclude_members([
        DummyUser(1),
        DummyUser(2),
        DummyUser(668226181769986078),
    ])) == [
        DummyUser(1),
        DummyUser(2),
    ]


def test_exclude_members_explicit():
    assert list(club.exclude_members([
        DummyUser(1),
        DummyUser(2),
        DummyUser(3),
        DummyUser(668226181769986078),
    ], [2, 3])) == [
        DummyUser(1),
        DummyUser(668226181769986078),
    ]
