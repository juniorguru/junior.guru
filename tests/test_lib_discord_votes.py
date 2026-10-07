from types import SimpleNamespace

from jg.coop.lib import discord_votes


def test_count_upvotes():
    reactions = [
        SimpleNamespace(emoji=SimpleNamespace(name="plus_one"), count=4),
        SimpleNamespace(emoji="👍", count=1),
        SimpleNamespace(emoji="🐣", count=3),
    ]
    assert discord_votes.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [
        SimpleNamespace(emoji="🙁", count=4),
        SimpleNamespace(emoji="👎", count=1),
        SimpleNamespace(emoji="🐣", count=3),
    ]
    assert discord_votes.count_downvotes(reactions) == 1
