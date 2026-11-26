from pathlib import Path

import pytest

from jg.coop.lib.discord_markdown import (
    discord_markdown_to_html,
    to_discord_markdown,
    truncate_discord_markdown,
)


fixtures = [
    pytest.param(path, id=path.stem) for path in Path(__file__).parent.glob("*.html")
]
assert len(fixtures) > 0, "No fixtures found"


@pytest.mark.parametrize("html_path", fixtures)
def test_to_discord_markdown(html_path: Path):
    html = html_path.read_text()
    expected = html_path.with_suffix(".md").read_text()

    assert to_discord_markdown(html) == expected


def test_truncate_discord_markdown_preserves_newlines():
    text = "Pracovni nabidka\n\n## Titulek\nAhoj"

    assert truncate_discord_markdown(text, max_length=10) == "Pracovni…"


def test_truncate_discord_markdown_does_not_change_short_text():
    text = "Pracovni nabidka\n\n## Titulek\nAhoj"

    assert truncate_discord_markdown(text, max_length=200) == text


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Ahoj", "<p>Ahoj</p>"),
        ("**Python** a *SQL*", "<p><strong>Python</strong> a <em>SQL</em></p>"),
        ("Řádek\nDalší řádek", "<p>Řádek<br>\nDalší řádek</p>"),
        ("Ahoj <@123456>!", "<p>Ahoj @někdo!</p>"),
        ("Ahoj <@!123456>!", "<p>Ahoj @někdo!</p>"),
        ("Pro <@&123456>", "<p>Pro @role</p>"),
        ("Viz <#123456>", "<p>Viz #kanál</p>"),
        ("Super <:python:123456> věc <a:party:654321>", "<p>Super  věc </p>"),
        ("Do <t:1767225600:D>", "<p>Do 1. 1. 2026</p>"),
        ("Do <t:1767225600>", "<p>Do 1. 1. 2026</p>"),
        ("-# Drobné písmo", "<p>Drobné písmo</p>"),
        ("<script>alert(1)</script>", "<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>"),
    ],
)
def test_discord_markdown_to_html(text: str, expected: str):
    assert discord_markdown_to_html(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "Viz https://example.com/job.",
            '<p>Viz <a href="https://example.com/job">https://example.com/job</a>.</p>',
        ),
        (
            "Viz <https://example.com/job>",
            '<p>Viz <a href="https://example.com/job">https://example.com/job</a></p>',
        ),
        (
            "Viz [inzerát](https://example.com/job)",
            '<p>Viz <a href="https://example.com/job">inzerát</a></p>',
        ),
    ],
)
def test_discord_markdown_to_html_links(text: str, expected: str):
    assert discord_markdown_to_html(text) == expected


def test_discord_markdown_to_html_list_right_after_paragraph():
    text = "Požadujeme:\n- Python\n- SQL"

    assert discord_markdown_to_html(text) == (
        "<p>Požadujeme:</p>\n<ul>\n<li>Python</li>\n<li>SQL</li>\n</ul>"
    )


def test_discord_markdown_to_html_headings_fit_into_job_card():
    assert discord_markdown_to_html("# Pozice") == '<h4 id="pozice">Pozice</h4>'
