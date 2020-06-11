import hashlib
from datetime import date, datetime

import pytest

from juniorguru.fetch.lib import jobs_sheet


@pytest.mark.parametrize('value,expected', [
    (None, None),
    ('12/13/2019 9:17:57', datetime(2019, 12, 13, 9, 17, 57)),
    ('8/6/2019 14:08:49', datetime(2019, 8, 6, 14, 8, 49)),
])
def test_coerce_datetime(value, expected):
    assert jobs_sheet.coerce_datetime(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    ('12/13/2019 9:17:57', date(2019, 12, 13)),
    ('8/6/2019 14:08:49', date(2019, 8, 6)),
    ('8/6/2019', date(2019, 8, 6)),
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


def test_create_id():
    id_ = jobs_sheet.create_id(datetime(2019, 7, 6, 20, 24, 3), 'https://www.example.com/foo/bar.html')
    assert id_ == hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest()


def test_coerce_record():
    assert jobs_sheet.coerce_record({
        'Timestamp': '7/6/2019 20:24:03',
        'Email Address': 'jobs@example.com',
        'Company name': 'Honza Ltd.',
        'Company website link': 'https://www.example.com',
        'Employment type': 'internship, full-time',
        'Job title': 'Frontend Ninja',
        'Job description': None,
        'Job location': 'Prague',
        'Job link': 'https://jobs.example.com/1245/',
        'Approved': None,
        'Sent': '11/11/2019',
        'Expired': '12/12/2019',
    }) == {
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
        'approved_at': None,
        'is_sent': True,
        'expired_at': date(2019, 12, 12),
        'source': 'juniorguru',
    }
