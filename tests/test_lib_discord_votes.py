from juniorguru.lib import discord_votes


class StubReaction:
    def __init__(self, emoji: str, count: int):
        self.emoji = emoji
        self.count = count


class StubEmoji:
    def __init__(self, name: str):
        self.name = name


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
