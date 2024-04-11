import pytest

from project.lib.remove_emoji import remove_emoji


@pytest.mark.parametrize(
    "text",
    [
        "❗Kurz Programátor www aplikací❗",
        "🦸🏻 Kurz Programátor www aplikací 🦸🏻",
        "  🦸🏻 Kurz Programátor www aplikací 🦸🏻  ",
        "🦸🏻  Kurz Programátor www aplikací  🦸🏻",
    ],
)
def test_remove_emoji(text):
    assert remove_emoji(text) == "Kurz Programátor www aplikací"


@pytest.mark.parametrize(
    "text",
    [
        "\u200dQA Engineer/Tester",
        "  \u200dQA Engineer/Tester",
        "\u200d  QA Engineer/Tester",
    ],
)
def test_remove_emoji_zero_width_joiner(text):
    assert remove_emoji(text) == "QA Engineer/Tester"
