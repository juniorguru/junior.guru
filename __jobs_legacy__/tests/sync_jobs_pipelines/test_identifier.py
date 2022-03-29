import pytest

from juniorguru.jobs.legacy_jobs.pipelines.identifier import Pipeline, MissingIdentifyingField


def test_identifier_keeps_id_set_by_spider(item, spider):
    item['id'] = '44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9'
    item = Pipeline().process_item(item, spider)

    assert item['id'] == '44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9'


def test_identifier_keeps_id_set_by_spider_even_if_link_missing(item, spider):
    item['id'] = '44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9'
    del item['link']
    item = Pipeline().process_item(item, spider)

    assert item['id'] == '44df50581c3a0c67657c40a587c22a19e10d414b593fcfaea5b01ae9'


def test_identifier_sets_default_id(item, spider):
    del item['id']
    item['link'] = 'https://example.com/we-are-hiring/123'
    item = Pipeline().process_item(item, spider)

    assert item['id'] == '69711e603674f2aacc2596fa7dc00bc0c4d5846ce838babe4f446b36'


def test_identifier_drops(item, spider):
    del item['id']
    del item['link']

    with pytest.raises(MissingIdentifyingField, match='link'):
        Pipeline().process_item(item, spider)
