import pytest

from juniorguru.sync.companies import coerce_record, parse_slug


def test_coerce_record_slug():
    record = coerce_record({'Coupon': 'COUPON12345678'})

    assert record['coupon'] == 'COUPON12345678'
    assert record['slug'] == 'coupon'


def test_coerce_record_slug_no_coupon():
    record = coerce_record({})

    assert 'slug' not in record


@pytest.mark.parametrize('coupon, expected', [
    (None, None),
    ('BANANA12345678', 'banana'),
])
def test_slug(coupon, expected):
    assert parse_slug(coupon) == expected
