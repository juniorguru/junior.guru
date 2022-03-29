from juniorguru.sync.jobs_scraped.pipelines.emoji_cleaner import process


def test_emoji_cleaner():
    item = process(dict(title='🦸🏻 Junior projekťák 🦸🏻'))

    assert item['title'] == 'Junior projekťák'
