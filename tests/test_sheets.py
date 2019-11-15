import hashlib
from datetime import datetime

import pytest

from juniorguru import sheets


@pytest.mark.parametrize('value,expected', [
    (None, None),
    ('7/6/2019 20:24:03', datetime(2019, 7, 6, 20, 24, 3)),
    ('8/30/2019 20:24:03', datetime(2019, 8, 30, 20, 24, 3)),
    ('11/11/2019 20:24:03', datetime(2019, 11, 11, 20, 24, 3)),
])
def test_coerce_timestamp(value, expected):
    assert sheets.coerce_timestamp(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, None),
    (' Foo Ltd.   ', 'Foo Ltd.'),
])
def test_coerce_text(value, expected):
    assert sheets.coerce_text(value) == expected


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
    assert sheets.coerce_boolean_words(value) == expected


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
    assert sheets.coerce_boolean(value) == expected


@pytest.mark.parametrize('value,expected', [
    (None, []),
    ('web frontend, mainstream programming language', ['mainstream programming language', 'web frontend'])
])
def test_coerce_set(value, expected):
    assert sheets.coerce_set(value) == expected


def test_create_id():
    id_ = sheets.create_id(datetime(2019, 7, 6, 20, 24, 3), 'https://www.example.com/foo/bar.html')
    assert id_ == hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest()


def test_coerce_record():
    assert sheets.coerce_record({
        'Timestamp': '7/6/2019 20:24:03',
        'Company name': 'Honza Ltd.',
        'Job type': 'paid internship',
        'Title': 'Frontend Ninja',
        'Company website link': 'https://www.example.com',
        'Email Address': 'jobs@example.com',
        'Location': 'Prague',
        'Description': None,
        'The applicant should ideally know basics of...': 'web frontend, mainstream programming language',
        'Approved': None
    }) == {
        'id': hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest(),
        'timestamp': datetime(2019, 7, 6, 20, 24, 3),
        'company_name': 'Honza Ltd.',
        'job_type': 'paid internship',
        'title': 'Frontend Ninja',
        'company_link': 'https://www.example.com',
        'email': 'jobs@example.com',
        'location': 'Prague',
        'description': None,
        'requirements': ['mainstream programming language', 'web frontend'],
        'is_approved': False
    }
