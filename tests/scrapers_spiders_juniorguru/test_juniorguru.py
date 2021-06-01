import hashlib
from datetime import datetime, date

import pytest
from scrapy.http import HtmlResponse

from juniorguru.scrapers.spiders import juniorguru


def create_record(record=None):
    record = record or {}
    return {
        'Timestamp': record.get('Timestamp', '7/6/2019 20:24:03'),
        'Email Address': record.get('Email Address', 'jobs@example.com'),
        'Název firmy': record.get('Název firmy', 'Honza Ltd.'),
        'Odkaz na webové stránky firmy': record.get('Odkaz na webové stránky firmy', 'https://www.example.com'),
        'Pracovní poměr': record.get('Pracovní poměr', 'internship, full-time'),
        'Nadpis pracovní nabídky': record.get('Nadpis pracovní nabídky', 'Frontend Ninja'),
        'Text pracovní nabídky': record.get('Text pracovní nabídky', None),
        'Je práce na dálku?': record.get('Je práce na dálku?', 'No'),
        'Město, kde se nachází kancelář': record.get('Město, kde se nachází kancelář', 'Prague'),
        'Externí odkaz na pracovní nabídku': record.get('Externí odkaz na pracovní nabídku', 'https://jobs.example.com/1245/'),
        'Varianta z ceníku': record.get('Varianta z ceníku', '0 CZK — Community'),
        'Approved': record.get('Approved', '10/10/2019'),
        'Expires': record.get('Expires', '12/12/2019'),
    }


def test_spider_parse():
    class Spider(juniorguru.Spider):
        def _get_records(self):
            return [
                create_record({'Město, kde se nachází kancelář': 'Praha'}),
                create_record({'Město, kde se nachází kancelář': 'Brno'}),
            ]

    response = HtmlResponse('https://example.com/', body=b'...')
    jobs = list(Spider().parse(response))

    assert len(jobs) == 2


def test_spider_parse_multiple_locations():
    class Spider(juniorguru.Spider):
        def _get_records(self):
            return [
                create_record({'Město, kde se nachází kancelář': 'Praha nebo Ostrava'}),
                create_record({'Město, kde se nachází kancelář': 'Brno'}),
            ]

    response = HtmlResponse('https://example.com/', body=b'...')
    jobs = list(Spider().parse(response))

    assert len(jobs) == 2
    assert jobs[0]['locations_raw'] == ['Praha', 'Ostrava']
    assert jobs[1]['locations_raw'] == ['Brno']


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
    id_ = hashlib.sha224(b'2019-07-06T20:24:03 www.example.com').hexdigest()
    assert juniorguru.coerce_record(create_record()) == {
        'id': id_,
        'posted_at': datetime(2019, 7, 6, 20, 24, 3),
        'email': 'jobs@example.com',
        'company_name': 'Honza Ltd.',
        'company_link': 'https://www.example.com',
        'employment_types': frozenset(['internship', 'full-time']),
        'title': 'Frontend Ninja',
        'locations_raw': ['Prague'],
        'remote': False,
        'link': f'https://junior.guru/jobs/{id_}/',
        'pricing_plan': 'community',
        'approved_at': date(2019, 10, 10),
        'expires_at': date(2019, 12, 12),
        'external_link': 'https://jobs.example.com/1245/',
    }
