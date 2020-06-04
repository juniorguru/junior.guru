import random
from datetime import date, datetime, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job


def shuffled(sorted_iterable):
    value = sorted_iterable[:]
    while True:
        random.shuffle(value)
        if value != sorted_iterable:
            break
    return value


@pytest.fixture
def db_connection():
    db = SqliteDatabase(':memory:')
    with db:
        Job.bind(db)
        Job.create_table()
        yield db
        Job.drop_table()


def create_job(id, **kwargs):
    return Job.create(
        id=str(id),
        posted_at=kwargs.get('posted_at', datetime(2019, 7, 6, 20, 24, 3)),
        company_name=kwargs.get('company_name', 'Honza Ltd.'),
        employment_types=kwargs.get('employment_types', frozenset(['internship'])),
        title=kwargs.get('title', 'Junior Software Engineer'),
        company_link=kwargs.get('company_link', 'https://example.com'),
        email=kwargs.get('email', 'recruiter@example.com'),
        location=kwargs.get('location', 'Brno, Czech Republic'),
        description=kwargs.get('description', '**Really long** description.'),
        source=kwargs.get('source', 'juniorguru'),
        approved_at=kwargs.get('approved_at', date.today()),
        is_sent=kwargs.get('is_sent', False),
        expired_at=kwargs.get('expired_at', None),
        jg_rank=kwargs.get('jg_rank'),
    )


def test_employment_types_are_unique_sorted_lists(db_connection):
    job = create_job('1', employment_types=['part-time', 'full-time', 'part-time'])

    assert Job.get_by_id('1').employment_types == ['full-time', 'part-time']


def test_employment_types_sorts_from_the_most_to_the_least_serious(db_connection):
    sorted_value = [
        'full-time',
        'part-time',
        'contract',
        'paid internship',
        'unpaid internship',
        'internship',
        'volunteering',
    ]
    job = create_job('1', employment_types=shuffled(sorted_value))

    assert Job.get_by_id('1').employment_types == sorted_value


def test_employment_types_sorts_extra_types_last_alphabetically(db_connection):
    job = create_job('1', employment_types=[
        'ahoj',
        'full-time',
        'bob',
        'part-time',
        'foo',
    ])

    assert Job.get_by_id('1').employment_types == [
        'full-time',
        'part-time',
        'ahoj',
        'bob',
        'foo',
    ]


def test_listing_returns_only_approved_jobs(db_connection):
    job1 = create_job('1', approved_at=date(1987, 8, 30))
    job2 = create_job('2', approved_at=None)
    job3 = create_job('3', approved_at=date(1987, 8, 30))

    assert set(Job.listing()) == {job1, job3}


def test_listing_returns_only_not_expired_jobs(db_connection):
    job1 = create_job('1', expired_at=None)
    job2 = create_job('2', expired_at=date(1987, 8, 30))
    job3 = create_job('3', expired_at=date.today())
    job4 = create_job('4', expired_at=date.today() + timedelta(days=2))

    assert set(Job.listing()) == {job1, job4}


def test_listing_sorts_by_posted_at_desc(db_connection):
    job1 = create_job('1', posted_at=datetime(2010, 7, 6, 20, 24, 3))
    job2 = create_job('2', posted_at=datetime(2019, 7, 6, 20, 24, 3))
    job3 = create_job('3', posted_at=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Job.listing()) == [job2, job3, job1]


def test_newsletter_listing_returns_only_approved_jobs(db_connection):
    job1 = create_job('1', approved_at=date(1987, 8, 30))
    job2 = create_job('2', approved_at=None)
    job3 = create_job('3', approved_at=date(1987, 8, 30))

    assert set(Job.newsletter_listing(5)) == {job1, job3}


def test_newsletter_listing_returns_only_not_expired_jobs(db_connection):
    job1 = create_job('1', expired_at=None)
    job2 = create_job('2', expired_at=date(1987, 8, 30))
    job3 = create_job('3', expired_at=date.today())
    job4 = create_job('4', expired_at=date.today() + timedelta(days=2))

    assert set(Job.newsletter_listing(5)) == {job1, job4}


def test_newsletter_listing_returns_only_jobs_not_sent(db_connection):
    job1 = create_job('1', is_sent=True)
    job2 = create_job('2', is_sent=False)
    job3 = create_job('3', is_sent=True)

    assert set(Job.newsletter_listing(5)) == {job2}


def test_newsletter_listing_sorts_by_posted_at_asc(db_connection):
    job1 = create_job('1', posted_at=datetime(2010, 7, 6, 20, 24, 3))
    job2 = create_job('2', posted_at=datetime(2019, 7, 6, 20, 24, 3))
    job3 = create_job('3', posted_at=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Job.newsletter_listing(5)) == [job1, job3, job2]


def test_newsletter_listing_returns_only_jg_if_enough(db_connection):
    job1 = create_job('1', source='juniorguru')
    job2 = create_job('2', source='moo')
    job3 = create_job('3', source='juniorguru')
    job4 = create_job('4', source='juniorguru')

    assert list(Job.newsletter_listing(3)) == [job1, job3, job4]


def test_newsletter_listing_backfills_with_other_sources(db_connection):
    job1 = create_job('1', source='moo', jg_rank=5)
    job2 = create_job('2', source='foo', jg_rank=-5)
    job3 = create_job('3', source='bar', jg_rank=10)
    job4 = create_job('4', source='juniorguru')
    job5 = create_job('5', source='juniorguru')

    assert list(Job.newsletter_listing(5)) == [job4, job5, job3, job1]


def test_newsletter_listing_backfills_up_to_min_count(db_connection):
    job1 = create_job('1', source='moo', jg_rank=5)
    job2 = create_job('2', source='foo', jg_rank=1)
    job3 = create_job('3', source='bar', jg_rank=10)
    job4 = create_job('4', source='juniorguru')

    assert list(Job.newsletter_listing(3)) == [job4, job3, job1]


def test_count(db_connection):
    create_job('1', approved_at=date(1987, 8, 30))
    create_job('2', approved_at=None)
    create_job('3', approved_at=date(1987, 8, 30))
    create_job('4', approved_at=date(1987, 8, 30), expired_at=date(1987, 9, 1))

    assert Job.count() == 2


def test_companies_count(db_connection):
    create_job('1', company_link='https://abc.example.com', approved_at=date(1987, 8, 30))
    create_job('2', company_link='https://abc.example.com', approved_at=None)
    create_job('3', company_link='https://xyz.example.com', approved_at=date(1987, 8, 30))
    create_job('4', company_link='https://xyz.example.com', approved_at=None)
    create_job('5', company_link='https://def.example.com', approved_at=None)
    create_job('6', company_link='https://def.example.com', approved_at=date(1987, 8, 30), expired_at=date(1987, 9, 1))

    assert Job.companies_count() == 2
