import random
from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job, JobMetric
from testing_utils import prepare_job_data


def shuffled(sorted_iterable):
    value = sorted_iterable[:]
    while True:
        random.shuffle(value)
        if value != sorted_iterable:
            break
    return value


def create_job(id, **kwargs):
    return Job.create(**prepare_job_data(id, **kwargs))


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
    create_job('1', employment_types=['part-time', 'full-time', 'part-time'])

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
    create_job('1', employment_types=shuffled(sorted_value))

    assert Job.get_by_id('1').employment_types == sorted_value


def test_employment_types_sorts_extra_types_last_alphabetically(db_connection):
    create_job('1', employment_types=[
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


def test_listing_sorts_by_junior_rank_desc(db_connection):
    job1 = create_job('1', junior_rank=10)
    job2 = create_job('2', junior_rank=30)
    job3 = create_job('3', junior_rank=20)

    assert list(Job.listing()) == [job2, job3, job1]


def test_listing_sorts_by_junior_rank_and_posted_at_desc(db_connection):
    job1 = create_job('1', junior_rank=5, posted_at=date(2010, 7, 3))
    job2 = create_job('2', junior_rank=5, posted_at=date(2019, 7, 6))
    job3 = create_job('3', junior_rank=5, posted_at=date(2014, 7, 5))

    assert list(Job.listing()) == [job2, job3, job1]


def test_juniorguru_listing(db_connection):
    job1 = create_job('1', source='juniorguru', junior_rank=30)
    job2 = create_job('2', source='moo')  # noqa
    job3 = create_job('3', source='juniorguru', junior_rank=20)
    job4 = create_job('4', source='juniorguru', junior_rank=10)

    assert list(Job.juniorguru_listing()) == [job1, job3, job4]


def test_juniorguru_listing_sorts_by_junior_rank_and_posted_at_desc(db_connection):
    job1 = create_job('1', source='juniorguru', junior_rank=5, posted_at=date(2010, 7, 3))
    job2 = create_job('2', source='juniorguru', junior_rank=5, posted_at=date(2019, 7, 6))
    job3 = create_job('3', source='juniorguru', junior_rank=5, posted_at=date(2014, 7, 5))
    job4 = create_job('4', source='moo')  # noqa

    assert list(Job.juniorguru_listing()) == [job2, job3, job1]


@pytest.mark.parametrize('source', [
    'juniorguru',
    'moo',
])
def test_newsletter_listing_sorts_by_junior_rank_desc(db_connection, source):
    job1 = create_job('1', source=source, junior_rank=30)
    job2 = create_job('2', source=source, junior_rank=10)
    job3 = create_job('3', source=source, junior_rank=20)

    assert list(Job.newsletter_listing(5)) == [job1, job3, job2]


@pytest.mark.parametrize('source', [
    'juniorguru',
    'moo',
])
def test_newsletter_listing_sorts_by_junior_rank_and_posted_at_desc(db_connection, source):
    job1 = create_job('1', source=source, junior_rank=5, posted_at=date(2020, 7, 10))
    job2 = create_job('2', source=source, junior_rank=5, posted_at=date(2020, 7, 6))
    job3 = create_job('3', source=source, junior_rank=5, posted_at=date(2020, 7, 8))

    assert list(Job.newsletter_listing(5)) == [job1, job3, job2]


def test_newsletter_listing_returns_only_juniorguru_if_enough(db_connection):
    job1 = create_job('1', source='juniorguru', junior_rank=30)
    job2 = create_job('2', source='moo')  # noqa
    job3 = create_job('3', source='juniorguru', junior_rank=20)
    job4 = create_job('4', source='juniorguru', junior_rank=10)

    assert list(Job.newsletter_listing(3)) == [job1, job3, job4]


def test_newsletter_listing_backfills_with_other_sources(db_connection):
    job1 = create_job('1', source='moo', junior_rank=20)
    job2 = create_job('2', source='foo', junior_rank=10)
    job3 = create_job('3', source='bar', junior_rank=40)
    job4 = create_job('4', source='juniorguru', junior_rank=30)
    job5 = create_job('5', source='juniorguru', junior_rank=20)

    assert list(Job.newsletter_listing(5)) == [job4, job5, job3, job1, job2]


def test_newsletter_listing_backfills_up_to_min_count(db_connection):
    job1 = create_job('1', source='moo', junior_rank=5)
    job2 = create_job('2', source='foo', junior_rank=1)  # noqa
    job3 = create_job('3', source='bar', junior_rank=10)
    job4 = create_job('4', source='juniorguru')

    assert list(Job.newsletter_listing(3)) == [job4, job3, job1]


def test_count(db_connection):
    create_job('1')
    create_job('2')
    create_job('3')
    create_job('4')

    assert Job.count() == 4


def test_companies_count(db_connection):
    create_job('1', company_link='https://abc.example.com')
    create_job('2', company_link='https://abc.example.com')
    create_job('3', company_link='https://xyz.example.com')
    create_job('4', company_link='https://xyz.example.com')
    create_job('5', company_link='https://def.example.com')
    create_job('6', company_link='https://def.example.com')

    assert Job.companies_count() == 3


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
    JobMetric.create(job=job1, name='users', value=3)
    JobMetric.create(job=job1, name='pageviews', value=6)
    job2 = create_job('2')
    JobMetric.create(job=job2, name='users', value=1)
    JobMetric.create(job=job2, name='pageviews', value=4)
    JobMetric.create(job=job2, name='applications', value=2)

    assert job1.metrics == {
        'users': 3,
        'pageviews': 6,
        'applications': 0,
    }
    assert job2.metrics == {
        'users': 1,
        'pageviews': 4,
        'applications': 2,
    }


def test_days_since_posted():
    job = Job(**prepare_job_data('1', posted_at=date(1987, 8, 30)))

    assert job.days_since_posted(today=date(1987, 9, 8)) == 9


def test_days_until_expires():
    job = Job(**prepare_job_data('1', expires_at=date(1987, 9, 8)))

    assert job.days_until_expires(today=date(1987, 8, 30)) == 9


@pytest.mark.parametrize('today,expected', [
    pytest.param(date(2020, 6, 20), False, id='not soon'),
    pytest.param(date(2020, 6, 21), True, id='10 days before'),
    pytest.param(date(2020, 6, 24), True, id='week before'),
    pytest.param(date(2020, 6, 26), True, id='random date in the middle'),
    pytest.param(date(2020, 6, 30), True, id='day before'),
    pytest.param(date(2020, 7, 1), True, id='the same day'),
])
def test_expires_soon(today, expected):
    job = Job(**prepare_job_data('1', expires_at=date(2020, 7, 1)))

    assert job.expires_soon(today=today) is expected
