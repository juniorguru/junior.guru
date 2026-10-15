from textwrap import dedent

import pytest

from jg.coop.lib.newsletter_content import (
    NewsletterContent,
    content_to_html,
    edit_content_html,
    get_linked_item_text,
    get_meetups_count,
    get_recording_title,
    get_section,
    get_story_headline,
    parse_newsletter,
)


CONTENT_HTML = dedent(
    """
        <h2>Plánované online akce</h2>
        <p><a href="https://junior.guru/events/66/">Od zdrojáku ke strojáku</a></p>
        <h2 id="srazy">Srazy, konference a jiné akce</h2>
        <p><strong>3.10. Brno</strong>, komunita:<br>
        <a href="https://example.com/1">Sraz 1</a></p>
        <p><strong>6.10. Praha</strong>, komunita:<br>
        <a href="https://example.com/2">Sraz 2</a></p>
        <p>O těchto akcích se psalo v <a href="https://junior.guru/club/">klubu</a>:</p>
        <p>▪️ <a href="https://discord.com/channels/1/2/3">Akce z Discordu</a></p>
        <h2>Nepřibarvené příběhy juniorů</h2>
        <p>▪️ Na pohovoru proti mně sedělo šest lidí. Tomáš Novák o\xa0tranzitu z\xa0hudby do\xa0IT – <a href="https://junior.guru/stories/tomas-novak/">Přečti</a><br>
        ▪️ Volalo mi padesát vymahačů denně, říká Lucie Kopecká – <a href="https://junior.guru/stories/lucie-kopecka/">Přečti</a></p>
        <h2>Záznamy z online akcí</h2>
        <p>▪️ Martin Rapavý: Jak fungují jazykové\xa0modely: Úvod – <a href="https://junior.guru/events/65/#zaznam">Sleduj</a><br>
        ▪️ Adina Fox: Designování vysněné práce – <a href="https://junior.guru/events/4/#zaznam">Sleduj</a></p>
        <h2>Co se dělo v klubu</h2>
        <p><a href="https://junior.guru/events/1/">Akce</a></p>
    """
)

CONTENT_HTML_EMPTY_SECTIONS = dedent(
    """
        <h2>Srazy, konference a jiné akce</h2>
        <p>Nic</p>
        <h2>Nepřibarvené příběhy juniorů</h2>
        <p>Nic</p>
        <h2>Záznamy z online akcí</h2>
        <p>Nic</p>
    """
)


def test_parse_newsletter():
    content = parse_newsletter(CONTENT_HTML)

    assert (
        content.meetups_count,
        content.story_headline,
        content.recording_title,
    ) == (
        2,
        "Na pohovoru proti mně sedělo šest lidí. Tomáš Novák o tranzitu z hudby do IT",
        "Jak fungují jazykové modely: Úvod",
    )


def test_get_description():
    content = parse_newsletter(CONTENT_HTML)

    assert content.get_description("Září 2026 ve světě IT juniorů") == (
        "Shrnutí pro juniory v IT za září 2026: 2 akce kam přijít, "
        "příběh „Na pohovoru proti mně sedělo šest lidí. "
        "Tomáš Novák o tranzitu z hudby do IT“, "
        "záznam z akce „Jak fungují jazykové modely: Úvod“"
    )


@pytest.mark.parametrize(
    "meetups_count, expected",
    [(1, " 1 akce kam"), (3, " 3 akce kam"), (5, " 5 akcí kam")],
)
def test_get_description_plurals(meetups_count: int, expected: str):
    content = NewsletterContent(
        html="",
        reading_time=1,
        meetups_count=meetups_count,
        story_headline="Příběh",
        recording_title="Záznam",
    )

    assert expected in content.get_description("Říjen 2025 ve světě IT juniorů")


def test_get_description_unexpected_subject():
    content = parse_newsletter(CONTENT_HTML)

    with pytest.raises(ValueError):
        content.get_description("Newsletter ve světě IT juniorů")


def test_parse_newsletter_missing_section():
    with pytest.raises(ValueError):
        parse_newsletter("<h2>Podcast</h2><p>Text</p>")


def test_get_section():
    section = get_section(CONTENT_HTML, "Záznamy z online akcí")

    assert [el.tag for el in section] == ["p"]


def test_get_section_missing():
    with pytest.raises(ValueError):
        get_section(CONTENT_HTML, "Neexistující sekce")


def test_get_meetups_count():
    assert get_meetups_count(CONTENT_HTML) == 2


def test_get_story_headline():
    assert get_story_headline(CONTENT_HTML) == (
        "Na pohovoru proti mně sedělo šest lidí. Tomáš Novák o tranzitu z hudby do IT"
    )


def test_get_recording_title():
    assert get_recording_title(CONTENT_HTML) == "Jak fungují jazykové modely: Úvod"


def test_get_recording_title_without_speaker():
    content_html = (
        "<h2>Záznamy z online akcí</h2>"
        '<p>▪️ Bez řečníka – <a href="https://junior.guru/events/1/">Sleduj</a></p>'
    )

    with pytest.raises(ValueError):
        get_recording_title(content_html)


def test_get_linked_item_text_custom_heading_and_url_prefix():
    content_html = (
        "<h2>Videa</h2>"
        '<p>▪️ <em>První</em> – <a href="https://junior.guru/stories/jana/">Jana</a><br>'
        '▪️ <em>Druhé</em> video – <a href="https://example.com/talks/42/">Talk</a></p>'
    )

    assert (
        get_linked_item_text(content_html, "Videa", "example.com/talks/")
        == "Druhé video"
    )


@pytest.mark.parametrize(
    "get_value", [get_meetups_count, get_story_headline, get_recording_title]
)
def test_get_value_from_empty_section(get_value):
    with pytest.raises(ValueError):
        get_value(CONTENT_HTML_EMPTY_SECTIONS)


@pytest.mark.parametrize(
    "get_value", [get_meetups_count, get_story_headline, get_recording_title]
)
def test_get_value_from_missing_section(get_value):
    with pytest.raises(ValueError):
        get_value("<h2>Podcast</h2><p>Text</p>")


def test_content_to_html_with_markdown():
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

    assert content_to_html(body) == expected


def test_content_to_html_with_html():
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

    assert content_to_html(body) == body


def test_edit_content_html_removes_double_br():
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

    assert edit_content_html(body) == expected


def test_edit_content_html_preserves_chart():
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
    assert edit_content_html(chart) == chart


def test_edit_content_html_strips_emoji_from_h2():
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

    assert edit_content_html(body) == expected


def test_edit_content_html_adds_trailing_slash_to_course_urls():
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

    assert edit_content_html(body) == expected


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
        get_story_headline(content_html)


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
        get_recording_title(content_html)
