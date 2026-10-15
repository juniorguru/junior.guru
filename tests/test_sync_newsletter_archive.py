from textwrap import dedent

import pytest

from jg.coop.sync.newsletter_archive import (
    get_issue_description,
    get_meetups_count,
    get_recording_event_id,
    get_section,
    get_story_slug,
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
        <p>▪️ Příběh – <a href="https://junior.guru/stories/tomas-novak/">Přečti</a><br>
        ▪️ Příběh – <a href="https://junior.guru/stories/lucie-kopecka/">Přečti</a></p>
        <h2>Záznamy z online akcí</h2>
        <p>▪️ Záznam – <a href="https://junior.guru/events/65/#zaznam">Sleduj</a><br>
        ▪️ Záznam – <a href="https://junior.guru/events/17/#zaznam">Sleduj</a></p>
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


def test_get_section():
    section = get_section(CONTENT_HTML, "Záznamy z online akcí")

    assert [el.tag for el in section] == ["p"]


def test_get_section_missing():
    with pytest.raises(ValueError):
        get_section(CONTENT_HTML, "Neexistující sekce")


def test_get_meetups_count():
    assert get_meetups_count(CONTENT_HTML) == 2


def test_get_story_slug():
    assert get_story_slug(CONTENT_HTML) == "tomas-novak"


def test_get_recording_event_id():
    assert get_recording_event_id(CONTENT_HTML) == 65


def test_get_story_slug_custom_heading_and_url_prefix():
    content_html = (
        "<h2>Příběhy</h2>"
        '<p><a href="https://junior.guru/events/1/">Akce</a> '
        '<a href="https://example.com/people/jana-nova/">Jana</a></p>'
    )

    assert (
        get_story_slug(
            content_html, heading="Příběhy", url_prefix="example.com/people/"
        )
        == "jana-nova"
    )


def test_get_recording_event_id_custom_heading_and_url_prefix():
    content_html = (
        "<h2>Videa</h2>"
        '<p><a href="https://junior.guru/stories/jana/">Jana</a> '
        '<a href="https://example.com/talks/42/">Talk</a></p>'
    )

    assert (
        get_recording_event_id(
            content_html, heading="Videa", url_prefix="example.com/talks/"
        )
        == 42
    )


@pytest.mark.parametrize(
    "get_value", [get_meetups_count, get_story_slug, get_recording_event_id]
)
def test_get_value_from_empty_section(get_value):
    with pytest.raises(ValueError):
        get_value(CONTENT_HTML_EMPTY_SECTIONS)


@pytest.mark.parametrize(
    "get_value", [get_meetups_count, get_story_slug, get_recording_event_id]
)
def test_get_value_from_missing_section(get_value):
    with pytest.raises(ValueError):
        get_value("<h2>Podcast</h2><p>Text</p>")


def test_get_issue_description():
    description = get_issue_description(
        "Září 2026 ve světě IT juniorů",
        11,
        "Tomáš Novák",
        "Jak fungují jazykové\xa0modely",
    )

    assert description == (
        "Shrnutí pro juniory v IT za září 2026: 11 akcí kam přijít, "
        "Tomáš Novák o své cestě do IT, "
        "záznam z akce „Jak fungují jazykové modely“"
    )


@pytest.mark.parametrize(
    "meetups_count, expected",
    [(1, " 1 akce kam"), (3, " 3 akce kam"), (5, " 5 akcí kam")],
)
def test_get_issue_description_plurals(meetups_count: int, expected: str):
    description = get_issue_description(
        "Říjen 2025 ve světě IT juniorů", meetups_count, "Nina", "Akce"
    )

    assert expected in description


def test_get_issue_description_unexpected_subject():
    with pytest.raises(ValueError):
        get_issue_description("Newsletter ve světě IT juniorů", 1, "Nina", "Akce")
