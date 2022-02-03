import pytest

from juniorguru.jobs.legacy_jobs.pipelines.language_filter import (IrrelevantLanguage,
                                                           Pipeline)


@pytest.mark.parametrize('lang', ['cs', 'en'])
def test_language_filter(item, spider, lang):
    item['lang'] = lang
    item = Pipeline().process_item(item, spider)

    assert item['lang'] == lang


@pytest.mark.parametrize('lang', ['de', 'fr', 'pl'])
def test_language_filter_drops(item, spider, lang):
    item['lang'] = lang

    with pytest.raises(IrrelevantLanguage, match=lang):
        Pipeline().process_item(item, spider)
