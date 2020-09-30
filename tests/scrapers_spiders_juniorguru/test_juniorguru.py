import hashlib
from datetime import datetime, date

import pytest

from juniorguru.scrapers.spiders import juniorguru


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
def test_parse_pricing_plan(value, expected):
    assert juniorguru.parse_pricing_plan(value) == expected


def test_create_id():
    id_ = juniorguru.create_id(datetime(2019, 7, 6, 20, 24, 3), 'https://www.example.com/foo/bar.html')
    assert id_ == hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest()


def test_coerce_record():
    assert juniorguru.coerce_record(create_record()) == {
        'id': hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest(),
        'posted_at': datetime(2019, 7, 6, 20, 24, 3),
        'email': 'jobs@example.com',
        'company_name': 'Honza Ltd.',
        'company_link': 'https://www.example.com',
        'employment_types': frozenset(['internship', 'full-time']),
        'title': 'Frontend Ninja',
        'location': 'Prague',
        'remote': False,
        'link': 'https://jobs.example.com/1245/',
        'pricing_plan': 'community',
        'approved_at': date(2019, 10, 10),
        'expires_at': date(2019, 12, 12),
    }


@pytest.mark.parametrize('value,expected', [
    (None, None),
    (' **Foo Ltd.**   ', '<p><strong>Foo Ltd.</strong></p>'),
])
def test_parse_markdown(value, expected):
    assert juniorguru.parse_markdown(value) == expected
