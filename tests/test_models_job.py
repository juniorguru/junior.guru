from datetime import datetime

import pytest
import random
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
def db():
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
        is_approved=kwargs.get('is_approved', True),
        is_sent=kwargs.get('is_sent', False),
        is_expired=kwargs.get('is_expired', False),
    )


def test_employment_types_are_unique_sorted_lists(db):
    job = create_job('1', employment_types=['part-time', 'full-time', 'part-time'])

    assert Job.get_by_id('1').employment_types == ['full-time', 'part-time']


def test_employment_types_sorts_from_the_most_to_the_least_serious(db):
    sorted_value = [
        'full-time',
        'part-time',
        'paid internship',
        'unpaid internship',
        'internship',
        'volunteering',
    ]
    job = create_job('1', employment_types=shuffled(sorted_value))

    assert Job.get_by_id('1').employment_types == sorted_value


def test_employment_types_sorts_extra_types_last_alphabetically(db):
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


def test_listing_returns_only_approved_jobs(db):
    job1 = create_job('1', is_approved=True)
    job2 = create_job('2', is_approved=False)
    job3 = create_job('3', is_approved=True)

    assert set(Job.listing()) == {job1, job3}


def test_listing_returns_only_not_expired_jobs(db):
    job1 = create_job('1', is_expired=False)
    job2 = create_job('2', is_expired=True)
    job3 = create_job('3', is_expired=False)

    assert set(Job.listing()) == {job1, job3}


def test_listing_sorts_by_posted_at_desc(db):
    job1 = create_job('1', posted_at=datetime(2010, 7, 6, 20, 24, 3))
    job2 = create_job('2', posted_at=datetime(2019, 7, 6, 20, 24, 3))
    job3 = create_job('3', posted_at=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Job.listing()) == [job2, job3, job1]


def test_newsletter_listing_returns_only_approved_jobs(db):
    job1 = create_job('1', is_approved=True)
    job2 = create_job('2', is_approved=False)
    job3 = create_job('3', is_approved=True)

    assert set(Job.newsletter_listing()) == {job1, job3}


def test_newsletter_listing_returns_only_jobs_not_sent(db):
    job1 = create_job('1', is_sent=True)
    job2 = create_job('2', is_sent=False)
    job3 = create_job('3', is_sent=True)

    assert set(Job.newsletter_listing()) == {job2}


def test_newsletter_listing_sorts_by_posted_at_asc(db):
    job1 = create_job('1', posted_at=datetime(2010, 7, 6, 20, 24, 3))
    job2 = create_job('2', posted_at=datetime(2019, 7, 6, 20, 24, 3))
    job3 = create_job('3', posted_at=datetime(2014, 7, 6, 20, 24, 3))

    assert list(Job.newsletter_listing()) == [job1, job3, job2]


def test_count_takes_only_approved_jobs(db):
    create_job('1', is_approved=True)
    create_job('2', is_approved=False)
    create_job('3', is_approved=True)

    assert Job.count() == 2


def test_companies_count_takes_only_approved_jobs(db):
    create_job('1', company_link='https://abc.example.com', is_approved=True)
    create_job('2', company_link='https://abc.example.com', is_approved=False)
    create_job('3', company_link='https://xyz.example.com', is_approved=True)
    create_job('4', company_link='https://xyz.example.com', is_approved=False)
    create_job('5', company_link='https://def.example.com', is_approved=False)

    assert Job.companies_count() == 2
