from pathlib import Path

from jg.coop.cli.update_feminine_names import format_names, parse_wiki_names


FIXTURES_DIR = Path(__file__).parent / "cli_update_feminine_names"


def test_parse_wiki_names():
    page_html = (FIXTURES_DIR / "wiki.html").read_text()

    assert parse_wiki_names(page_html) == [
        "Jana",
        "Marie",
        "Eva",
        "Evženie",
        "Mirka",
        "Jasmína",
    ]


def test_format_names():
    assert format_names(["Marie", "Anna", "Marie"]) == "Anna\nMarie\n"
