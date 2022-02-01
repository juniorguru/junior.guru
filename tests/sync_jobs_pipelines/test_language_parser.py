from pathlib import Path

import pytest
from langdetect import DetectorFactory

from juniorguru.jobs.legacy_jobs.pipelines.language_parser import Pipeline
from testing_utils import param_startswith_skip, startswith_skip


DetectorFactory.seed = 0  # prevent non-deterministic language detection


def generate_params(fixtures_dirname):
    for path in (Path(__file__).parent / fixtures_dirname).rglob('*.html'):
        if startswith_skip(path):
            yield param_startswith_skip(path)
        else:
            name = path.name.split(path.suffix)[0]
            lang = name.split('_')[0]
            yield pytest.param(path.read_text(), lang, id=name)


@pytest.mark.parametrize('description_html,expected_lang',
                         generate_params('fixtures_language_parser'))
def test_language_parser(item, spider, description_html, expected_lang):
    item['description_html'] = description_html
    item = Pipeline().process_item(item, spider)

    assert item['lang'] == expected_lang
