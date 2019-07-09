from datetime import datetime

import pytest

from juniorguru.jobs import sheets


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
    (None, set()),
    ('mainstream programming language, web frontend', {'mainstream programming language', 'web frontend'})
])
def test_coerce_set(value, expected):
    assert sheets.coerce_set(value) == expected


def test_coerce_record():
    assert sheets.coerce_record({
        'Timestamp': '7/6/2019 20:24:03',
        'Company name': 'Honza Ltd.',
        'Job type': 'paid internship',
        'Title': 'Frontend Ninja',
        'Are you an employment agency?': 'no',
        'Company website link': 'http://honzajavorek.cz',
        'Email Address': 'mail@honzajavorek.cz',
        'Location': 'Prague',
        'Description': None,
        'The applicant should ideally know basics of...': 'mainstream programming language, web frontend',
        'Approved': None
    }) == {
        'timestamp': datetime(2019, 7, 6, 20, 24, 3),
        'company_name': 'Honza Ltd.',
        'job_type': 'paid internship',
        'title': 'Frontend Ninja',
        'is_agency': False,
        'company_link': 'http://honzajavorek.cz',
        'email': 'mail@honzajavorek.cz',
        'location': 'Prague',
        'description': None,
        'requirements': {'mainstream programming language', 'web frontend'},
        'is_approved': False
    }
