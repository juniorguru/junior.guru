from pathlib import Path

import pytest

from juniorguru.scrapers.pipelines.requirements_parser import Pipeline


def generate_requirements_parser_params(fixtures_dir):
    for path in (Path(__file__).parent / fixtures_dir).rglob('*.html'):
        expected = path.with_suffix('.txt').read_text().splitlines()
        yield pytest.param(path.read_text(),  # description_raw
                           expected,
                           id=path.name)  # ID for better readability


@pytest.mark.parametrize('description_raw,expected',
                         generate_requirements_parser_params('fixtures_description_parser'))
def test_requirements_parser(item, spider, description_raw, expected):
    item['description_raw'] = description_raw
    item = Pipeline().process_item(item, spider)

    assert sorted(item['requirements']) == sorted(expected)
