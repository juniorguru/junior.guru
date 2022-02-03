from juniorguru.jobs.legacy_jobs.pipelines.emoji_cleaner import Pipeline


def test_emoji_cleaner(item, spider):
    item['title'] = '🦸🏻 Junior projekťák 🦸🏻'
    item = Pipeline().process_item(item, spider)

    assert item['title'] == 'Junior projekťák'
