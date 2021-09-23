from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Employment


def create_employment(**data):
    data.setdefault('title', 'Junior Python Engineer')
    data.setdefault('company_name', 'Company Ltd.')
    data.setdefault('url', 'https://example.com/jobs/1')
    data.setdefault('apply_url', 'https://example.com/jobs/1?utm_source=123')
    data.setdefault('description_html', '<p>Needs to know some <strong>Python</strong>!</p>')
    data.setdefault('lang', 'en')
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
    return dict(title='Junior Python Engineer',
                company_name='Company Ltd.',
                url='https://example.com/jobs/123',
                description_html='<p>Needs to know some <strong>Python</strong>!</p>',
                lang='en',
                locations=[],
                seen_at=date.today(),
                source='exciting-job-board',
                source_urls=['https://api.example.com/jobs.xml'])


def test_get_by_item_url(db_connection):
    create_employment(title='Job 1', url='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', url='https://xyz.example.com/jobs/2')
    create_employment(title='Job 3', url='https://xyz.example.com/jobs/3')
    item = dict(url='https://xyz.example.com/jobs/2')
    employment = Employment.get_by_item(item)

    assert employment.title == 'Job 2'


def test_get_by_item_url_raises_does_not_exist(db_connection):
    create_employment(title='Job 1', url='https://xyz.example.com/jobs/1')
    create_employment(title='Job 2', url='https://xyz.example.com/jobs/2')
    item = dict(url='https://xyz.example.com/jobs/42')

    with pytest.raises(Employment.DoesNotExist):
        Employment.get_by_item(item)


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
    employment = create_employment(source_urls=[
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


def test_merge_item_when_item_is_newer(db_connection, item):
    employment = create_employment(last_seen_at=date(2021, 9, 1))
    item['seen_at'] = date(2021, 9, 15)
    item['title'] = 'New Title'
    item['company_name'] = 'New Company Name'
    item['apply_url'] = 'https://new.example.com/1?utm_source=123'
    item['locations'] = [dict(name='New Name', region='New Region')]
    item['description_html'] = '<p>New Description</p>'
    item['lang'] = 'nw'
    item['source'] = 'new-source'
    employment.merge_item(item)

    assert sorted([field.name for field in employment.dirty_fields]) == sorted([
        'title', 'company_name', 'locations', 'description_html', 'source', 'lang', 'apply_url',
        'last_seen_at', 'first_seen_at', 'source_urls', 'items_merged_count',
    ])
    assert employment.title == 'New Title'
    assert employment.company_name == 'New Company Name'
    assert employment.apply_url == 'https://new.example.com/1?utm_source=123'
    assert employment.locations == [dict(name='New Name', region='New Region')]
    assert employment.description_html == '<p>New Description</p>'
    assert employment.lang == 'nw'
    assert employment.source == 'new-source'


def test_merge_item_when_item_is_older(db_connection, item):
    employment = create_employment(last_seen_at=date(2021, 9, 1),
                                   title='Title',
                                   apply_url='https://example.com/1?utm_source=123',
                                   company_name='Company Name',
                                   locations=[dict(name='Name', region='Region')],
                                   description_html='<p>Description</p>',
                                   lang='en',
                                   source='source')
    item['seen_at'] = date(2021, 8, 15)
    employment.merge_item(item)

    assert sorted([field.name for field in employment.dirty_fields]) == sorted([
        'last_seen_at', 'first_seen_at', 'source_urls', 'items_merged_count',
    ])
    assert employment.title == 'Title'
    assert employment.company_name == 'Company Name'
    assert employment.apply_url == 'https://example.com/1?utm_source=123'
    assert employment.locations == [dict(name='Name', region='Region')]
    assert employment.description_html == '<p>Description</p>'
    assert employment.lang == 'en'
    assert employment.source == 'source'


def test_merge_item_bookkeeping(db_connection, item):
    employment = create_employment()

    assert employment.items_merged_count == 0

    employment.merge_item(item)
    employment.merge_item(item)
    employment.merge_item(item)

    assert employment.items_merged_count == 3
