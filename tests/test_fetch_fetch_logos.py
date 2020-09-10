import hashlib
from datetime import date

from juniorguru.fetch.fetch_logos import coerce_record


def create_record(record=None):
    record = record or {}
    return {
        'Name': record.get('Timestamp', 'Awesome Company'),
        'Email': record.get('Email Address', 'recruitment@example.com'),
        'Link': record.get('Link', 'https://example.com/landing-page'),
        'Link RegExp': record.get('Link RegExp', None),
        'Price': record.get('Price', 30000),
        'Months': record.get('Months', 12),
        'Job Slots': record.get('Job Slots', 2),
        'Starts': record.get('Starts', '2020-09-04'),
        'Expires': record.get('Expires', '2021-09-04'),
    }


def test_coerce_record():
    assert coerce_record(create_record()) == {
        'id': hashlib.sha224(b'Awesome Company').hexdigest(),
        'name': 'Awesome Company',
        'email': 'recruitment@example.com',
        'link': 'https://example.com/landing-page',
        'link_re': r'example\.com',
        'months': 12,
        'starts_at': date(2020, 9, 4),
        'expires_at': date(2021, 9, 4),
    }


def test_coerce_record_explicit_re():
    data = coerce_record(create_record({
        'Link RegExp': r'www\.example\.com|jobs\.example\.com',
    }))

    assert data['link_re'] == r'www\.example\.com|jobs\.example\.com'
