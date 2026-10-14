import pytest

from jg.coop.lib.text import emoji_url, remove_emoji, shorten_description


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


def test_shorten_description_short_text():
    assert shorten_description("  Krátký   popis.  ") == "Krátký popis."


def test_shorten_description_long_text():
    text = "Velmi dlouhá první věta, která se nevejde. Druhá věta."

    assert shorten_description(text, max_length=20) == "Velmi dlouhá první…"


def test_shorten_description_long_text_strips_punctuation():
    text = "Jedna, dva, tři, čtyři, pět."

    assert shorten_description(text, max_length=17) == "Jedna, dva, tři…"


def test_shorten_description_exact_length():
    assert shorten_description("Přesně tak.", max_length=11) == "Přesně tak."
