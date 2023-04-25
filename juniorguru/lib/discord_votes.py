from juniorguru.lib.discord_club import ClubEmoji, emoji_name


EMOJI_UPVOTES = [ClubEmoji.PIN,
                 '👍', '❤️', '😍', '🥰', '💕', '♥️', '💖', '💙', '💗', '💜', '💞', '💓', '💛', '🖤', '💚', '😻', '🧡', '👀',
                 '💯', '🤩', '😋', '💟', '🤍', '🤎', '💡', '👆', '👏', '🥇', '🏆', '✔️', 'plus_one', '👌', 'babyyoda', 'meowsheart',
                 'meowthumbsup', '✅', '🤘', 'this', 'dk', '🙇‍♂️', '🙇', '🙇‍♀️', 'kgsnice', 'successkid', 'white_check_mark', 'welldone',
                 'notbad', 'updoot', '🆒', '🔥', 'yayfrog', 'partyparrot', 'drakeyes', 'awyeah', 'meowparty',
                 '🫶', 'exactly']

EMOJI_DOWNVOTES = ['👎']


def count_upvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_UPVOTES])


def count_downvotes(reactions):
    return sum([reaction.count for reaction in reactions
                if emoji_name(reaction.emoji) in EMOJI_DOWNVOTES])
