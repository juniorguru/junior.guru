import json
from pathlib import Path

import pytest
from strictyaml import Map, Seq, Str, Url, load

from juniorguru.scrapers.pipelines.sections_parser import Pipeline


schema = Seq(
    Map({
        'heading': Str(),
        'bullets': Seq(Str()),
    })
)


def generate_sections_parser_params(fixtures_dir):
    for html_path in (Path(__file__).parent / fixtures_dir).rglob('*.html'):
        yaml_path = html_path.with_suffix('.yml')
        if yaml_path.is_file():
            yaml = load(yaml_path.read_text(), schema)
            # use json.loads/json.dumps to recursively convert all
            # ordered dicts to dicts, which significantly improves readability
            # of the pytest diff
            expected = json.loads(json.dumps(yaml.data))
            yield pytest.param(html_path.read_text(), expected,
                               id=html_path.name)  # better readability
        else:
            yield pytest.param('', '',
                               id=html_path.name,  # better readability
                               marks=pytest.mark.skip)


@pytest.mark.parametrize('description_raw,expected',
                         generate_sections_parser_params('fixtures_sections_parser'))
def test_sections_parser(item, spider, description_raw, expected):
    item['description_raw'] = description_raw
    item = Pipeline().process_item(item, spider)

    assert item['sections'] == expected
