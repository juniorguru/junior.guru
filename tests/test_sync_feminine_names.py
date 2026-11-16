from pathlib import Path

import pytest

from jg.coop.sync.feminine_names import get_variants, parse_names, remove_accents


DATA_PATH = Path(__file__).parent.parent / "src/jg/coop/data/feminine_names.txt"


def test_parse_names():
    assert parse_names("Anna\n  Eliška \n\nZoe\n") == ["Anna", "Eliška", "Zoe"]


def test_get_variants():
    assert get_variants(["Eliška", "Anna"]) == ["eliška", "eliska", "anna"]


def test_get_variants_deduplicates():
    assert get_variants(["Adela", "Adéla"]) == ["adela", "adéla"]


@pytest.mark.parametrize(
    "s, expected",
    [
        ("žluťoučký", "zlutoucky"),
        ("ľudmila", "ludmila"),
        ("anna", "anna"),
    ],
)
def test_remove_accents(s: str, expected: str):
    assert remove_accents(s) == expected


def test_data_file_contains_common_names():
    names = parse_names(DATA_PATH.read_text())

    assert {"Jana", "Eva", "Lindice"} <= set(names)
