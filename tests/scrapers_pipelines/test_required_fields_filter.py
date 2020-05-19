import pytest

from juniorguru.scrapers.pipelines.required_fields_filter import (
    MissingRequiredFields, Pipeline)


def test_required_fields_filter(item, spider):
    Pipeline().process_item(item, spider)


def test_required_fields_drops(item, spider):
    del item['posted_at']
    del item['description_html']

    with pytest.raises(MissingRequiredFields, match=f'description_html, posted_at'):
        Pipeline().process_item(item, spider)
