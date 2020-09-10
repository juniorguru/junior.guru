import hashlib
from datetime import date, datetime

import pytest

from juniorguru.fetch.lib import jobs_sheet


def create_record(record=None):
    record = record or {}
    return {
        'Timestamp': record.get('Timestamp', '7/6/2019 20:24:03'),
        'Email Address': record.get('Email Address', 'jobs@example.com'),
        'Company name': record.get('Company name', 'Honza Ltd.'),
        'Company website link': record.get('Company website link', 'https://www.example.com'),
        'Employment type': record.get('Employment type', 'internship, full-time'),
        'Job title': record.get('Job title', 'Frontend Ninja'),
        'Job description': record.get('Job description', None),
        'Job location': record.get('Job location', 'Prague'),
        'Job link': record.get('Job link', 'https://jobs.example.com/1245/'),
        'Pricing plan': record.get('Pricing plan', '0 CZK — Community'),
        'Approved': record.get('Approved', '10/10/2019'),
        'Expires': record.get('Expires', '12/12/2019'),
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
    assert jobs_sheet.coerce_datetime(value) == expected


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
    assert jobs_sheet.coerce_date(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    (' Foo Ltd.   ', 'Foo Ltd.'),
])
def test_coerce_text(value, expected):
    assert jobs_sheet.coerce_text(value) == expected


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
    assert jobs_sheet.coerce_boolean_words(value) == expected


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
    assert jobs_sheet.coerce_boolean(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, frozenset()),
    ('', frozenset()),
    (', ,', frozenset()),
    ('web frontend, bash', frozenset(['bash', 'web frontend'])),
    ('internship', frozenset(['internship'])),
])
def test_coerce_set(value, expected):
    assert jobs_sheet.coerce_set(value) == expected


@pytest.mark.parametrize('value,expected', [
    ('5000 CZK — Annual Flat Rate, first posting (Roční paušál, první inzerát)', 'annual_flat_rate'),
    ('0 CZK — Annual Flat Rate (Roční paušál)', 'annual_flat_rate'),
    ('500 CZK — Standard', 'standard'),
    ('690 CZK — Standard', 'standard'),
    ('600 CZK', 'standard'),
    ('0 CZK', 'community'),
    ('0 CZK — Community', 'community'),
    ('', 'community'),
    (None, 'community'),
])
def test_coerce_pricing_plan(value, expected):
    assert jobs_sheet.coerce_pricing_plan(value) == expected


def test_create_id():
    id_ = jobs_sheet.create_id(datetime(2019, 7, 6, 20, 24, 3), 'https://www.example.com/foo/bar.html')
    assert id_ == hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest()


def test_coerce_record():
    assert jobs_sheet.coerce_record(create_record()) == {
        'id': hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest(),
        'posted_at': datetime(2019, 7, 6, 20, 24, 3),
        'email': 'jobs@example.com',
        'company_name': 'Honza Ltd.',
        'company_link': 'https://www.example.com',
        'employment_types': frozenset(['internship', 'full-time']),
        'title': 'Frontend Ninja',
        'description': None,
        'location': 'Prague',
        'link': 'https://jobs.example.com/1245/',
        'pricing_plan': 'community',
        'approved_at': date(2019, 10, 10),
        'expires_at': date(2019, 12, 12),
        'source': 'juniorguru',
    }


@pytest.mark.parametrize('approved,expires,expected', [
    (None, None, None),
    ('6/23/2020', None, date(2020, 7, 23)),
    ('6/23/2020', '6/30/2020', date(2020, 6, 30)),
])
def test_coerce_record_expires(approved, expires, expected):
    data = jobs_sheet.coerce_record(create_record({
        'Approved': approved,
        'Expires': expires,
    }))

    assert data['expires_at'] == expected
