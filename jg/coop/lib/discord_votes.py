from jg.coop.lib.discord_club import ClubEmoji, emoji_name


EMOJI_UPVOTES = [
    "♥️",
    "✅",
    "✔️",
    "❤️",
    "🏆",
    "👀",
    "👆",
    "👌",
    "👍",
    "👏",
    "💓",
    "💕",
    "💖",
    "💗",
    "💙",
    "💚",
    "💛",
    "💜",
    "💞",
    "💟",
    "💡",
    "💪",
    "💯",
    "🔥",
    "🖤",
    "🤍",
    "🤎",
    "🤘",
    "🤩",
    "🥇",
    "🥰",
    "🧡",
    "🫶",
    "😋",
    "😍",
    "😻",
    "🙇",
    "🙇‍♀️",
    "🙇‍♂️",
    "awyeah",
    "babyyoda",
    "🆒",
    "dk",
    "drakeyes",
    "exactly",
    "kgsnice",
    "meowparty",
    "meowsheart",
    "meowthumbsup",
    "notbad",
    "partyparrot",
    "plus_one",
    "successkid",
    "this",
    "updoot",
    "welldone",
    "white_check_mark",
    "yayfrog",
    ClubEmoji.PIN,
]

EMOJI_DOWNVOTES = ["👎"]


def count_upvotes(reactions):
    return sum(
        [
            reaction.count
            for reaction in reactions
            if emoji_name(reaction.emoji) in EMOJI_UPVOTES
        ]
    )


def count_downvotes(reactions):
    return sum(
        [
            reaction.count
            for reaction in reactions
            if emoji_name(reaction.emoji) in EMOJI_DOWNVOTES
        ]
    )
