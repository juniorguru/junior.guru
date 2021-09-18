from datetime import date, timedelta
from operator import itemgetter

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Employment


def create_employment(**data):
    data.setdefault('title', 'Junior Python Engineer')
    data.setdefault('company_name', 'Company Ltd.')
    data.setdefault('url', 'https://example.com/jobs/1')
    data.setdefault('alternative_urls', [
        'https://example.com/jobs/1?utm_source=123',
        'https://jobboard.example.com/abcdefgh/1234',
    ])
    data.setdefault('description_html', '<p>Needs to know some <strong>Python</strong>!</p>')
    data.setdefault('first_seen_at', date.today() - timedelta(weeks=1))
    data.setdefault('last_seen_at', date.today())
    data.setdefault('source', 'exciting-job-board')
    data.setdefault('source_urls', [
        'https://api.example.com/jobs.xml',
        'https://app.circleci.com/pipelines/github/honzajavorek/junior.guru/3528/workflows/7e41e9f4-23b1-44cb-8bc3-a5b8ce8b2694/jobs/21310',
    ])
    return Employment.create(**data)


@pytest.fixture
def db_connection():
    models = [Employment]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


@pytest.fixture
def item():
    return dict(alternative_urls=[],
                locations=[],
                seen_at=date.today(),
                source_urls=[])


def test_get_by_item_finds_url_by_url(db_connection):
    create_employment(title='Job 1', url='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', url='https://xyz.example.com/jobs/2')
    create_employment(title='Job 3', url='https://xyz.example.com/jobs/3')
    item = dict(url='https://xyz.example.com/jobs/2')
    employment = Employment.get_by_item(item)

    assert employment.title == 'Job 2'


def test_get_by_item_finds_url_by_alternative_url(db_connection):
    create_employment(title='Job 1', url='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', url='https://xyz.example.com/jobs/2')
    create_employment(title='Job 3', url='https://xyz.example.com/jobs/3')
    item = dict(alternative_urls=['https://xyz.example.com/jobs/2'])
    employment = Employment.get_by_item(item)

    assert employment.title == 'Job 2'


def test_get_by_item_finds_alternative_url_by_url(db_connection):
    create_employment(title='Job 1', alternative_urls='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', alternative_urls='https://xyz.example.com/jobs/2')
    create_employment(title='Job 3', alternative_urls='https://xyz.example.com/jobs/3')
    item = dict(url='https://xyz.example.com/jobs/2')
    employment = Employment.get_by_item(item)

    assert employment.title == 'Job 2'


def test_get_by_item_finds_alternative_url_by_alternative_url(db_connection):
    create_employment(title='Job 1', alternative_urls='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', alternative_urls='https://xyz.example.com/jobs/2')
    create_employment(title='Job 3', alternative_urls='https://xyz.example.com/jobs/3')
    item = dict(alternative_urls=['https://xyz.example.com/jobs/2'])
    employment = Employment.get_by_item(item)

    assert employment.title == 'Job 2'


def test_get_by_item_raises_does_not_exist_error(db_connection):
    create_employment(title='Job 1', url='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', url='https://xyz.example.com/jobs/2')
    item = dict(url='https://xyz.example.com/jobs/42')

    with pytest.raises(Employment.DoesNotExist):
        Employment.get_by_item(item)


def test_merge_item_alternative_urls(db_connection, item):
    employment = create_employment(title='Job 1', alternative_urls=[
        'https://abc.example.com/jobs/1',
        'https://xyz.example.com/jobs/1',
    ])
    item['alternative_urls'] = [
        'https://abc.example.com/jobs/1',
        'https://efg.example.com/jobs/1',
    ]
    employment.merge_item(item)

    assert sorted(employment.alternative_urls) == [
        'https://abc.example.com/jobs/1',
        'https://efg.example.com/jobs/1',
        'https://xyz.example.com/jobs/1',
    ]


@pytest.mark.parametrize('employment_seen_at, item_seen_at, expected', [
    (date(2021, 10, 1), date(2021, 5, 1), date(2021, 5, 1)),
    (date(2021, 5, 1), date(2021, 10, 1), date(2021, 5, 1)),
])
def test_merge_item_first_seen_at(db_connection, item, employment_seen_at, item_seen_at, expected):
    employment = create_employment(first_seen_at=employment_seen_at)
    item['seen_at'] = item_seen_at
    employment.merge_item(item)

    assert employment.first_seen_at == expected


@pytest.mark.parametrize('employment_seen_at, item_seen_at, expected', [
    (date(2021, 10, 1), date(2021, 5, 1), date(2021, 10, 1)),
    (date(2021, 5, 1), date(2021, 10, 1), date(2021, 10, 1)),
])
def test_merge_item_last_seen_at(db_connection, item, employment_seen_at, item_seen_at, expected):
    employment = create_employment(last_seen_at=employment_seen_at)
    item['seen_at'] = item_seen_at
    employment.merge_item(item)

    assert employment.last_seen_at == expected


def test_merge_item_source_urls(db_connection, item):
    employment = create_employment(title='Job 1', source_urls=[
        'https://abc.example.com/jobs/1',
        'https://xyz.example.com/jobs/1',
    ])
    item['source_urls'] = [
        'https://abc.example.com/jobs/1',
        'https://efg.example.com/jobs/1',
    ]
    employment.merge_item(item)

    assert sorted(employment.source_urls) == [
        'https://abc.example.com/jobs/1',
        'https://efg.example.com/jobs/1',
        'https://xyz.example.com/jobs/1',
    ]


def test_merge_item_locations(db_connection, item):
    employment = create_employment(title='Job 1', locations=[
        {'name': 'Kladno', 'region': 'Prague'},
        {'name': 'Ivančice', 'region': 'Brno'},
    ])
    item['locations'] = [
        {'name': 'Kladno', 'region': 'Prague'},
        {'name': 'Tečovice', 'region': 'Zlín'},
    ]
    employment.merge_item(item)

    assert sorted(employment.locations, key=itemgetter('name')) == [
        {'name': 'Ivančice', 'region': 'Brno'},
        {'name': 'Kladno', 'region': 'Prague'},
        {'name': 'Tečovice', 'region': 'Zlín'},
    ]
