import pytest

from jg.coop.lib.text import emoji_url, remove_emoji


@pytest.mark.parametrize(
    "text",
    [
        "❗Kurz Programátor www aplikací❗",
        "🦸🏻 Kurz Programátor www aplikací 🦸🏻",
        "  🦸🏻 Kurz Programátor www aplikací 🦸🏻  ",
        "🦸🏻  Kurz Programátor www aplikací  🦸🏻",
    ],
)
def test_remove_emoji(text: str):
    assert remove_emoji(text) == "Kurz Programátor www aplikací"


@pytest.mark.parametrize(
    "text",
    [
        "\u200dQA Engineer/Tester",
        "  \u200dQA Engineer/Tester",
        "\u200d  QA Engineer/Tester",
    ],
)
def test_remove_emoji_zero_width_joiner(text: str):
    assert remove_emoji(text) == "QA Engineer/Tester"


@pytest.mark.parametrize(
    "emoji, expected",
    [
        ("❤️", "https://jdecked.github.io/twemoji/v/latest/72x72/2764.png"),
        ("3️⃣", "https://jdecked.github.io/twemoji/v/latest/72x72/33-20e3.png"),
    ],
)
def test_emoji_url(emoji: str, expected: str):
    assert emoji_url(emoji) == expected
