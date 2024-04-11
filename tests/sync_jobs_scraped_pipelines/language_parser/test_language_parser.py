import asyncio
from pathlib import Path

import pytest

from coop.lib.text import extract_text
from coop.sync.jobs_scraped.pipelines.language_parser import (
    parse_language,
    process,
)


fixtures = [
    pytest.param(extract_text(path.read_text()), path.stem.split("_")[0], id=path.name)
    for path in (Path(__file__).parent).rglob("*.html")
]
assert len(fixtures) > 0, "No fixtures found"


@pytest.mark.parametrize("description_text, expected_lang", fixtures)
@pytest.mark.asyncio
async def test_language_parser_process(description_text: str, expected_lang: str):
    item = await process(dict(description_text=description_text))

    assert item["lang"] == expected_lang


@pytest.mark.asyncio
async def test_language_parser_process_does_not_error_when_ran_in_parallel():
    results = await asyncio.gather(
        *[
            process(dict(description_text=extract_text(path.read_text())))
            for path in (Path(__file__).parent).rglob("*.html")
        ]
    )

    assert len(results) > 5, "Not enough fixtures to test parallelism"


@pytest.mark.parametrize("description_text, expected_lang", fixtures)
def test_language_parser_parse_language(description_text: str, expected_lang: str):
    assert parse_language(description_text) == expected_lang
