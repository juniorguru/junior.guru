import pytest

from juniorguru.sync.jobs_scraped.pipelines.emoji_cleaner import process


@pytest.mark.parametrize('title', [
    '🦸🏻 Junior projekťák 🦸🏻',
    '  🦸🏻 Junior projekťák 🦸🏻  ',
    '🦸🏻  Junior projekťák  🦸🏻',
])
def test_emoji_cleaner(title):
    item = process(dict(title=title))

    assert item['title'] == 'Junior projekťák'
