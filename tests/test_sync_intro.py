import pytest
from discord import Reaction

from juniorguru.sync.intro import get_missing_reactions


def create_reaction(emoji, me=True):
    return Reaction(message=None, data={'count': 42, 'me': me}, emoji=emoji)


@pytest.mark.parametrize('existing_reactions, ensure_emojis, expected', [
    ([create_reaction('❤️'), create_reaction('💬')],
     ['🤡', '🐣'],
     {'🤡', '🐣'}),
    ([create_reaction('🤡'), create_reaction('❤️'), create_reaction('💬')],
     ['🤡', '🐣'],
     {'🐣'}),
    ([create_reaction('🤡'), create_reaction('❤️'), create_reaction('🐣')],
     ['🤡', '🐣'],
     set()),
    ([],
     ['🤡', '🐣'],
     {'🤡', '🐣'}),
    ([create_reaction('🤡'), create_reaction('❤️'), create_reaction('🐣')],
     [],
     set()),
])
def test_get_missing_reactions(existing_reactions, ensure_emojis, expected):
    assert get_missing_reactions(existing_reactions, ensure_emojis) == expected
