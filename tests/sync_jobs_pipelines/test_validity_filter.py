from datetime import date

import pytest

from juniorguru.jobs.legacy_jobs.pipelines.validity_filter import (
    Pipeline, Expired, NotApproved)


def test_validity_filter_explicit_expiration(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 1)
    item['expires_at'] = date(2020, 10, 1)
    Pipeline(today=date(2020, 9, 15)).process_item(item, spider)


def test_validity_filter_explicit_expiration_drops(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 1)
    item['expires_at'] = date(2020, 10, 1)

    with pytest.raises(Expired, match='Expiration 2020-10-01 ≤ today 2020-10-02'):
        Pipeline(today=date(2020, 10, 2)).process_item(item, spider)


def test_validity_filter_implicit_expiration(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 1)
    item['expires_at'] = None
    item = Pipeline(today=date(2020, 9, 15)).process_item(item, spider)

    assert item['expires_at'] == date(2020, 10, 1)


def test_validity_filter_implicit_expiration_drops(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 1)
    item['expires_at'] = None

    with pytest.raises(Expired, match='Expiration 2020-10-01 ≤ today 2020-10-02'):
        Pipeline(today=date(2020, 10, 2)).process_item(item, spider)


def test_validity_filter_not_approved_drops(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = None

    with pytest.raises(NotApproved):
        Pipeline(today=date(2020, 9, 2)).process_item(item, spider)


def test_validity_filter_approved_at_used_as_posted_at(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 3)
    item = Pipeline(today=date(2020, 9, 5)).process_item(item, spider)

    assert item['posted_at'] == date(2020, 9, 3)
    assert item['approved_at'] == date(2020, 9, 3)


def test_validity_filter_approved_at_used_for_calculating_implicit_expiration(item, spider):
    item['posted_at'] = date(2020, 9, 1)
    item['approved_at'] = date(2020, 9, 3)
    item['expires_at'] = None
    item = Pipeline(today=date(2020, 9, 5)).process_item(item, spider)

    assert item['posted_at'] == date(2020, 9, 3)
    assert item['approved_at'] == date(2020, 9, 3)
    assert item['expires_at'] == date(2020, 10, 3)
