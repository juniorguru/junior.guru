from pathlib import Path
from textwrap import dedent

import pytest

from jg.coop.lib.newsletter_content_info import (
    NewsletterContentInfo,
    _get_linked_item_text,
    _get_meetups_count,
    _get_recording_title,
    _get_section,
    _get_story_headline,
    edit_newsletter_content_html,
    newsletter_content_to_html,
    parse_newsletter_content,
)


FIXTURES_DIR = Path(__file__).parent


def read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


@pytest.mark.parametrize(
    "fixture_name, expected",
    [
        (
            "newsletter_content_before_2025-12.html",
            (
                10,
                (
                    "Mnohdy ani sama firma nemá jasno v tom, koho chce nabrat, "
                    "říká vývojářka Nina"
                ),
                "DevOps/SRE - co to vlastně je a chci to vůbec vědět?",
            ),
        ),
        (
            "newsletter_content.md",
            (
                8,
                (
                    "Na pohovoru proti mně sedělo šest lidí. "
                    "Tomáš Novák o tranzitu z hudby do IT"
                ),
                "Jak fungují jazykové modely a co z toho plyne pro práci s nimi",
            ),
        ),
    ],
)
def test_parse_newsletter_content(fixture_name: str, expected: tuple):
    content_info = parse_newsletter_content(read_fixture(fixture_name))

    assert (
        content_info.meetups_count,
        content_info.story_headline,
        content_info.recording_title,
    ) == expected


def test_parse_newsletter_content_with_colon_in_recording_title():
    content_info = parse_newsletter_content(
        read_fixture("newsletter_content_with_colon_in_recording_title.md")
    )

    assert content_info.recording_title == (
        "Z diplomacie do jednorožce: Jak jsem se ocitl v IT bez řádku kódu"
    )


def test_parse_newsletter_content_missing_section():
    with pytest.raises(ValueError):
        parse_newsletter_content("<h2>Podcast</h2><p>Text</p>")


def test_get_description():
    content_info = parse_newsletter_content(read_fixture("newsletter_content.md"))

    assert content_info.get_description("Září 2026 ve světě IT juniorů") == (
        "Shrnutí pro juniory v IT za září 2026: 8 akcí kam přijít, "
        "příběh „Na pohovoru proti mně sedělo šest lidí. "
        "Tomáš Novák o tranzitu z hudby do IT“, "
        "záznam z akce „Jak fungují jazykové modely a co z toho plyne pro práci s nimi“"
    )


@pytest.mark.parametrize(
    "meetups_count, expected",
    [(1, " 1 akce kam"), (3, " 3 akce kam"), (5, " 5 akcí kam")],
)
def test_get_description_plurals(meetups_count: int, expected: str):
    content_info = NewsletterContentInfo(
        html="",
        reading_time=1,
        meetups_count=meetups_count,
        story_headline="Příběh",
        recording_title="Záznam",
    )

    assert expected in content_info.get_description("Říjen 2025 ve světě IT juniorů")


def test_get_description_unexpected_subject():
    content_info = NewsletterContentInfo(
        html="",
        reading_time=1,
        meetups_count=1,
        story_headline="Příběh",
        recording_title="Záznam",
    )

    with pytest.raises(ValueError):
        content_info.get_description("Newsletter ve světě IT juniorů")


def test_get_section():
    content_html = "<h2>A</h2><p>1</p><h2>B</h2><p>2</p><ul><li>3</li></ul><h2>C</h2>"
    section = _get_section(content_html, "B")

    assert [el.tag for el in section] == ["p", "ul"]


def test_get_section_missing():
    with pytest.raises(ValueError):
        _get_section("<h2>A</h2><p>1</p>", "B")


def test_get_recording_title_without_speaker():
    content_html = (
        "<h2>Záznamy z online akcí</h2>"
        '<p>▪️ Bez řečníka – <a href="https://junior.guru/events/1/">Sleduj</a></p>'
    )

    with pytest.raises(ValueError):
        _get_recording_title(content_html)


def test_get_linked_item_text_custom_heading_and_url_prefix():
    content_html = (
        "<h2>Videa</h2>"
        '<p>▪️ <em>První</em> – <a href="https://junior.guru/stories/jana/">Jana</a><br>'
        '▪️ <em>Druhé</em> video – <a href="https://example.com/talks/42/">Talk</a></p>'
    )

    assert (
        _get_linked_item_text(content_html, "Videa", "example.com/talks/")
        == "Druhé video"
    )


@pytest.mark.parametrize(
    "get_value", [_get_meetups_count, _get_story_headline, _get_recording_title]
)
def test_get_value_from_empty_section(get_value):
    content_html = dedent(
        """
            <h2>Srazy, konference a jiné akce</h2>
            <p>Nic</p>
            <h2>Nepřibarvené příběhy juniorů</h2>
            <p>Nic</p>
            <h2>Záznamy z online akcí</h2>
            <p>Nic</p>
        """
    )

    with pytest.raises(ValueError):
        get_value(content_html)


@pytest.mark.parametrize(
    "get_value", [_get_meetups_count, _get_story_headline, _get_recording_title]
)
def test_get_value_from_missing_section(get_value):
    with pytest.raises(ValueError):
        get_value("<h2>Podcast</h2><p>Text</p>")


def test_newsletter_content_to_html_with_markdown():
    body = dedent(
        """
            # Nadpis

            Toto je **tučný** text s [odkazem](https://example.com).

            - Položka 1
            - Položka 2
        """
    ).strip()
    expected = dedent(
        """
            <h1 id="nadpis">Nadpis</h1>
            <p>Toto je <strong>tučný</strong> text s <a href="https://example.com">odkazem</a>.</p>
            <ul>
            <li>Položka 1</li>
            <li>Položka 2</li>
            </ul>
        """
    ).strip()

    assert newsletter_content_to_html(body) == expected


def test_newsletter_content_to_html_with_html():
    body = dedent(
        """
            <h1>Nadpis</h1>
            <p>Toto je <strong>tučný</strong> text s <a href="https://example.com">odkazem</a>.</p>
            <ul>
            <li>Položka 1</li>
            <li>Položka 2</li>
            </ul>
        """
    ).strip()

    assert newsletter_content_to_html(body) == body


def test_edit_newsletter_content_html_removes_double_br():
    body = dedent(
        """
            <p>
            <strong>12.11. Brno</strong>, komunita kolem frontendu:<br>
            <br>
            <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.meetup.com/frontendisti/events/311580722/">Brno: Přístupný diskuzní večer</a>
            </p>
        """
    ).strip()
    expected = dedent(
        """
            <p>
            <strong>12.11. Brno</strong>, komunita kolem frontendu:<br>
            <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.meetup.com/frontendisti/events/311580722/">Brno: Přístupný diskuzní večer</a>
            </p>
        """
    ).strip()

    assert edit_newsletter_content_html(body) == expected


def test_edit_newsletter_content_html_preserves_chart():
    chart = dedent(
        """
            <p>
            🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨 81× #testing<br>
            🟨🟨🟨🟨🟨🟨🟨🟨🟨 78× #database<br>
            🟨🟨🟨🟨🟨🟨🟨 61× #javascript<br>
            🟨🟨🟨🟨🟨🟨 56× #python<br>
            🟨🟨🟨🟨🟨 46× #css<br>
            🟨🟨🟨🟨🟨 44× #html<br>
            🟨🟨🟨🟨🟨 41× #excel<br>
            🟨🟨🟨 31× #csharp<br>
            🟨🟨🟨 29× #git<br>
            🟨🟨 24× #linux<br>
            </p>
        """
    ).strip()
    assert edit_newsletter_content_html(chart) == chart


def test_edit_newsletter_content_html_strips_emoji_from_h2():
    body = dedent(
        """
            <h2>🚀 Nové kurzy a články</h2>
            <h2>🔥 Akce a meetupy</h2>
        """
    ).strip()
    expected = dedent(
        """
            <h2>Nové kurzy a články</h2>
            <h2>Akce a meetupy</h2>
        """
    ).strip()

    assert edit_newsletter_content_html(body) == expected


def test_edit_newsletter_content_html_adds_trailing_slash_to_course_urls():
    body = (
        '<a href="https://junior.guru/courses/engeto">Engeto</a> '
        '<a href="https://junior.guru/courses/42prague?utm_source=x">42</a> '
        '<a href="https://junior.guru/courses/czechitas/">Czechitas</a> '
        '<a href="https://junior.guru/courses/">Kurzy</a>'
    )
    expected = (
        '<a href="https://junior.guru/courses/engeto/">Engeto</a> '
        '<a href="https://junior.guru/courses/42prague/?utm_source=x">42</a> '
        '<a href="https://junior.guru/courses/czechitas/">Czechitas</a> '
        '<a href="https://junior.guru/courses/">Kurzy</a>'
    )

    assert edit_newsletter_content_html(body) == expected


@pytest.mark.parametrize(
    "item_html",
    [
        '▪️ – <a href="https://junior.guru/stories/jana/">Přečti</a>',
        '▪️ <a href="https://junior.guru/stories/jana/">Přečti</a>',
        '▪️ Text bez oddělovače <a href="https://junior.guru/stories/jana/">Přečti</a>',
    ],
)
def test_get_story_headline_unidentifiable(item_html: str):
    content_html = f"<h2>Nepřibarvené příběhy juniorů</h2><p>{item_html}</p>"

    with pytest.raises(ValueError):
        _get_story_headline(content_html)


@pytest.mark.parametrize(
    "text",
    ["Martin Rapavý:  ", ": Jak fungují jazykové modely"],
)
def test_get_recording_title_unidentifiable(text: str):
    content_html = (
        "<h2>Záznamy z online akcí</h2>"
        f'<p>▪️ {text} – <a href="https://junior.guru/events/1/">Sleduj</a></p>'
    )

    with pytest.raises(ValueError):
        _get_recording_title(content_html)
