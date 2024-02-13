from pathlib import Path

import pytest
from langdetect import DetectorFactory

from juniorguru.sync.jobs_scraped.pipelines.language_parser import (
    parse_language,
    process,
)


DetectorFactory.seed = 0  # prevent non-deterministic language detection


fixtures = [
    pytest.param(path.read_text(), path.stem.split("_")[0], id=path.name)
    for path in (Path(__file__).parent).rglob("*.html")
]
assert len(fixtures) > 0, "No fixtures found"


@pytest.mark.parametrize("description_html, expected_lang", fixtures)
@pytest.mark.asyncio
async def test_language_parser_process(description_html: str, expected_lang: str):
    item = await process(dict(description_html=description_html))

    assert item["lang"] == expected_lang


@pytest.mark.parametrize("description_html, expected_lang", fixtures)
def test_language_parser_parse_language(description_html: str, expected_lang: str):
    assert parse_language(description_html) == expected_lang
