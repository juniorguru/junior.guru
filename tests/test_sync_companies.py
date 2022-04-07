import pytest

from juniorguru.sync.companies import parse_slug, coerce_record


def test_coerce_record_slug():
    record = coerce_record({'Coupon Base': 'COUPON123'})

    assert record['coupon_base'] == 'COUPON123'
    assert record['slug'] == 'coupon'


def test_coerce_record_slug_no_coupon_base():
    record = coerce_record({})

    assert 'slug' not in record


@pytest.mark.parametrize('coupon_base, expected', [
    (None, None),
    ('BANANA123', 'banana'),
])
def test_slug(coupon_base, expected):
    assert parse_slug(coupon_base) == expected
