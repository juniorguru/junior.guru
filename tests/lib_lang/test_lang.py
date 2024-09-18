import asyncio
from pathlib import Path

import pytest

from jg.coop.lib.lang import async_parse_language, parse_language
from jg.coop.lib.text import extract_text


fixtures = [
    pytest.param(extract_text(path.read_text()), path.stem.split("_")[0], id=path.name)
    for path in (Path(__file__).parent).rglob("*.html")
]
assert len(fixtures) > 0, "No fixtures found"


@pytest.mark.asyncio
async def test_async_parse_language_does_not_error_when_ran_in_parallel():
    results = await asyncio.gather(
        *[
            async_parse_language(extract_text(path.read_text()))
            for path in (Path(__file__).parent).rglob("*.html")
        ]
    )

    assert len(results) > 5, "Not enough fixtures to test parallelism"


@pytest.mark.parametrize("description_text, expected_lang", fixtures)
def test_parse_language(description_text: str, expected_lang: str):
    assert parse_language(description_text) == expected_lang
