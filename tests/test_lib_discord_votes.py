from collections import namedtuple

from jg.core.lib import discord_votes


StubReaction = namedtuple("Reaction", ["emoji", "count"])

StubEmoji = namedtuple("Emoji", ["name"])


def test_count_upvotes():
    reactions = [
        StubReaction(StubEmoji("plus_one"), 4),
        StubReaction("👍", 1),
        StubReaction("🐣", 3),
    ]
    assert discord_votes.count_upvotes(reactions) == 5


def test_count_downvotes():
    reactions = [StubReaction("🙁", 4), StubReaction("👎", 1), StubReaction("🐣", 3)]
    assert discord_votes.count_downvotes(reactions) == 1
