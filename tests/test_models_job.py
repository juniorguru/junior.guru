import random
from datetime import date, datetime, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job, JobMetric
from testing_utils import create_job


def shuffled(sorted_iterable):
    value = sorted_iterable[:]
    while True:
        random.shuffle(value)
        if value != sorted_iterable:
            break
    return value


@pytest.fixture
def db_connection():
    models = [JobMetric, Job]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


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
    job1 = create_job('1', expires_at=None)
    job2 = create_job('2', expires_at=date(1987, 8, 30))
    job3 = create_job('3', expires_at=date.today())
    job4 = create_job('4', expires_at=date.today() + timedelta(days=2))

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
    job1 = create_job('1', expires_at=None)
    job2 = create_job('2', expires_at=date(1987, 8, 30))
    job3 = create_job('3', expires_at=date.today())
    job4 = create_job('4', expires_at=date.today() + timedelta(days=2))

    assert set(Job.newsletter_listing(5)) == {job1, job4}


def test_newsletter_listing_returns_only_jobs_not_sent(db_connection):
    job1 = create_job('1', newsletter_at=date.today() - timedelta(days=2))
    job2 = create_job('2', newsletter_at=None)
    job3 = create_job('3', newsletter_at=date.today() - timedelta(days=2))

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
    create_job('4', approved_at=date(1987, 8, 30), expires_at=date(1987, 9, 1))

    assert Job.count() == 2


def test_companies_count(db_connection):
    create_job('1', company_link='https://abc.example.com', approved_at=date(1987, 8, 30))
    create_job('2', company_link='https://abc.example.com', approved_at=None)
    create_job('3', company_link='https://xyz.example.com', approved_at=date(1987, 8, 30))
    create_job('4', company_link='https://xyz.example.com', approved_at=None)
    create_job('5', company_link='https://def.example.com', approved_at=None)
    create_job('6', company_link='https://def.example.com', approved_at=date(1987, 8, 30), expires_at=date(1987, 9, 1))

    assert Job.companies_count() == 2


def test_get_by_url(db_connection):
    job = create_job('1')

    assert Job.get_by_url('https://junior.guru/jobs/1/') == job


def test_get_by_url_raises_value_error(db_connection):
    with pytest.raises(ValueError):
        Job.get_by_url('https://example.com/jobs/xyz/')


def test_get_by_url_raises_does_not_exist_error(db_connection):
    with pytest.raises(Job.DoesNotExist):
        Job.get_by_url('https://junior.guru/jobs/1/')


def test_get_by_link(db_connection):
    job = create_job('1', link='https://example.com/1234')

    assert Job.get_by_link('https://example.com/1234') == job


def test_get_by_link_raises_does_not_exist_error(db_connection):
    with pytest.raises(Job.DoesNotExist):
        Job.get_by_link('https://example.com/1234')


def test_metrics(db_connection):
    job1 = create_job('1')
    metric1 = JobMetric.create(job=job1, name='users', value=3)
    metric2 = JobMetric.create(job=job1, name='pageviews', value=6)
    job2 = create_job('2')
    metric1 = JobMetric.create(job=job2, name='users', value=1)
    metric2 = JobMetric.create(job=job2, name='pageviews', value=4)

    assert job1.metrics == {
        'users': 3,
        'pageviews': 6,
        'applications': 0,
    }
    assert job2.metrics == {
        'users': 1,
        'pageviews': 4,
        'applications': 0,
    }
