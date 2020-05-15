from pathlib import Path

import pytest
from strictyaml import Enum, Map, Optional, Seq, Str, Url

from juniorguru.scrapers.pipelines import features_parser
from utils import load_yaml, param_startswith_skip, startswith_skip


schema = Seq(
    Map({
        Optional('heading'): Str(),
        'type': Enum(['paragraph', 'list']),
        'contents': Seq(Str()),
    })
)


def generate_params(fixtures_dirname):
    for path in (Path(__file__).parent / fixtures_dirname).rglob('*.yml'):
        if startswith_skip(path):
            yield param_startswith_skip(path)
        else:
            fixture = load_yaml(yml_path.read_text(), schema)
            yield pytest.param(fixture['sections'],
                               fixture['features'],
                               id=path.name)  # better readability


@pytest.mark.parametrize('sections,expected',
                         generate_params('fixtures_features_parser'))
def test_features_parser(item, spider, sections, expected):
    item['sections'] = sections
    item = features_parser.Pipeline().process_item(item, spider)

    assert item['features'] == expected
