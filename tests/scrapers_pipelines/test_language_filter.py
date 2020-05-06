import re
from pathlib import Path

import pytest
from langdetect import DetectorFactory

from juniorguru.scrapers.pipelines.language_filter import (IrrelevantLanguage,
                                                           Pipeline)


DetectorFactory.seed = 0  # prevent non-deterministic language detection


def generate_language_filter_params(fixtures_dir):
    for path in (Path(__file__).parent / fixtures_dir).rglob('*.html'):
        match = re.search(r'''
            ^(?P<id>                # test case ID for better readability
                (?P<lang>\w{2})     # expected language code
                ([^\.]+)?           # optional part describing the test case
            )\.html$                # file extension
        ''', path.name, re.VERBOSE)
        yield pytest.param(path.read_text(),  # description_raw
                           match.group('lang'),  # expected_lang
                           id=match.group('id'))  # ID for better readability


@pytest.mark.parametrize('description_raw,expected_lang',
                         generate_language_filter_params('fixtures_lang'))
def test_language_filter(item, spider, description_raw, expected_lang):
    item['description_raw'] = description_raw
    item = Pipeline().process_item(item, spider)

    assert item['lang'] == expected_lang


@pytest.mark.parametrize('description_raw,expected_lang',
                         generate_language_filter_params('fixtures_lang_raises'))
def test_language_filter_drops(item, spider, description_raw, expected_lang):
    item['description_raw'] = description_raw

    with pytest.raises(IrrelevantLanguage, match=expected_lang):
        Pipeline().process_item(item, spider)
