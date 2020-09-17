from datetime import date, datetime

import pytest

from juniorguru.lib import coerce


def test_coerce():
    assert coerce.coerce({
        r'^name$': ('name', coerce.parse_text),
        r'^numbers?$': ('number', coerce.parse_int),
        r'^start(s|ed)$': ('starts_at', coerce.parse_date),
        r'^count$': ('something', coerce.parse_int),
    }, {
        'Name': '\tHonza   ',
        'Number': '123   ',
        'Started': '2020-08-30',
        'Count': '',
    }) == {
        'name': 'Honza',
        'number': 123,
        'starts_at': date(2020, 8, 30),
    }


@pytest.mark.parametrize('value,expected', [
    (None, None),

    # default Google Sheets format
    ('12/13/2019 9:17:57', datetime(2019, 12, 13, 9, 17, 57)),
    ('8/6/2019 14:08:49', datetime(2019, 8, 6, 14, 8, 49)),

    # my custom setting
    ('2019-08-06 14:08:49', datetime(2019, 8, 6, 14, 8, 49)),
    ('2019-08-06 14:08:49+02:00', datetime(2019, 8, 6, 14, 8, 49)),
])
def test_coerce_datetime(value, expected):
    assert coerce.parse_datetime(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),

    # default Google Sheets format
    ('12/13/2019 9:17:57', date(2019, 12, 13)),
    ('8/6/2019 14:08:49', date(2019, 8, 6)),
    ('8/6/2019', date(2019, 8, 6)),

    # my custom setting
    ('2019-08-06 14:08:49', date(2019, 8, 6)),
    ('2019-08-06', date(2019, 8, 6)),
])
def test_coerce_date(value, expected):
    assert coerce.parse_date(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    (' Foo Ltd.   ', 'Foo Ltd.'),
])
def test_coerce_text(value, expected):
    assert coerce.parse_text(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    (' 123   ', 123),
    (345, 345),
    (345.01, 345),
])
def test_coerce_int(value, expected):
    assert coerce.parse_int(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    ('foo', None),
    ('1', None),
    ('True', None),
    ('true', None),
    ('yes', True),
    ('no', False),
])
def test_coerce_boolean_words(value, expected):
    assert coerce.parse_boolean_words(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, False),
    ('', False),
    ('foo', True),
    ('1', True),
    ('True', True),
    ('true', True),
    ('yes', True),
    ('no', True),
])
def test_coerce_boolean(value, expected):
    assert coerce.parse_boolean(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, frozenset()),
    ('', frozenset()),
    (', ,', frozenset()),
    ('web frontend, bash', frozenset(['bash', 'web frontend'])),
    ('internship', frozenset(['internship'])),
])
def test_coerce_set(value, expected):
    assert coerce.parse_set(value) == expected
