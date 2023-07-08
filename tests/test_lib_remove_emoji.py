import pytest

from juniorguru.lib.remove_emoji import remove_emoji


@pytest.mark.parametrize('title', [
    '❗Kurz Programátor www aplikací❗',
    '🦸🏻 Kurz Programátor www aplikací 🦸🏻',
    '  🦸🏻 Kurz Programátor www aplikací 🦸🏻  ',
    '🦸🏻  Kurz Programátor www aplikací  🦸🏻',
])
def test_remove_emoji(text):
    assert remove_emoji(text) == 'Kurz Programátor www aplikací'


@pytest.mark.parametrize('title', [
    '\u200dQA Engineer/Tester',
    '  \u200dQA Engineer/Tester',
    '\u200d  QA Engineer/Tester',
])
def test_remove_emoji_zero_width_joiner(text):
    assert text == 'QA Engineer/Tester'
