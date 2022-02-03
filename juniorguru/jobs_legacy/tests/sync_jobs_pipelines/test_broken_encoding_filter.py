from pathlib import Path

import pytest

from juniorguru.jobs.legacy_jobs.pipelines.broken_encoding_filter import (
    BrokenEncoding, Pipeline)
from testing_utils import param_startswith_skip, startswith_skip


def generate_params(fixtures_dirname):
    for path in (Path(__file__).parent / fixtures_dirname).rglob('*.html'):
        if startswith_skip(path):
            yield param_startswith_skip(path)
        else:
            yield pytest.param(path.read_text(), id=path.name)


@pytest.mark.parametrize('description_html',
                         generate_params('fixtures_broken_encoding_filter_raises'))
def test_broken_encoding_filter_raises(item, spider, description_html):
    item['description_html'] = description_html

    with pytest.raises(BrokenEncoding):
        Pipeline().process_item(item, spider)


@pytest.mark.parametrize('description_html',
                         generate_params('fixtures_broken_encoding_filter'))
def test_broken_encoding_filter(item, spider, description_html):
    item['description_html'] = description_html

    Pipeline().process_item(item, spider)
