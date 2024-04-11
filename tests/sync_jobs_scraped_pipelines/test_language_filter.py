import pytest

from jg.core.sync.jobs_scraped import DropItem
from jg.core.sync.jobs_scraped.pipelines.language_filter import process


@pytest.mark.parametrize("lang", ["cs", "en", "sk"])
@pytest.mark.asyncio
async def test_language_filter_lets_relevant_languages_through(lang: str):
    await process(dict(lang=lang))


@pytest.mark.parametrize("lang", ["es", "de", "fr"])
@pytest.mark.asyncio
async def test_language_filter_drops_irrelevant_languages(lang: str):
    with pytest.raises(DropItem):
        await process(dict(lang=lang))
