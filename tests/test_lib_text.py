from textwrap import dedent

import pytest

from jg.coop.lib.text import emoji_url, regenerate_html, remove_emoji


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


def test_regenerate_html_preserves_structure():
    html_text = dedent(
        """
        <html>
            <body>
                <footer><p>Footer text</p></footer>
                <dialog class="discord-dialog">
                    <p>Dialog</p>
                </dialog>
            </body>
        </html>
        """
    )

    html_gen = regenerate_html(html_text)
    html_soup = next(html_gen)
    html_text = html_gen.send(html_soup)
    html_gen.close()

    expected = dedent(
        """
        <html>
         <body>
          <footer>
           <p>
            Footer text
           </p>
          </footer>
          <dialog class="discord-dialog">
           <p>
            Dialog
           </p>
          </dialog>
         </body>
        </html>
        """
    ).lstrip()

    assert html_text == expected


def test_regenerate_html_does_not_entity_escape_czech():
    html_text = "<html><body><p>Čau a ahoj</p></body></html>"

    html_gen = regenerate_html(html_text)
    html_soup = next(html_gen)
    html_text = html_gen.send(html_soup)
    html_gen.close()

    assert "Čau" in html_text
    assert "&Ccaron;" not in html_text
