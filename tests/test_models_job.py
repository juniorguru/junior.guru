from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job, JobMetric
from testing_utils import prepare_job_data


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


def test_listing(db_connection):
    job1 = create_job('1', sort_rank=10)
    job2 = create_job('2', sort_rank=30)
    job3 = create_job('3', sort_rank=20)

    assert list(Job.listing()) == [job2, job3, job1]


def test_juniorguru_listing(db_connection):
    job1 = create_job('1', source='juniorguru', sort_rank=30)
    job2 = create_job('2', source='moo')  # noqa
    job3 = create_job('3', source='juniorguru', sort_rank=20)
    job4 = create_job('4', source='juniorguru', sort_rank=10)

    assert list(Job.juniorguru_listing()) == [job1, job3, job4]


@pytest.mark.parametrize('source', [
    'juniorguru',
    'moo',
])
def test_newsletter_listing_sorts_by_sort_rank_desc(db_connection, source):
    job1 = create_job('1', source=source, sort_rank=30)
    job2 = create_job('2', source=source, sort_rank=10)
    job3 = create_job('3', source=source, sort_rank=20)

    assert list(Job.newsletter_listing(5)) == [job1, job3, job2]


def test_newsletter_listing_returns_only_juniorguru_if_enough(db_connection):
    job1 = create_job('1', source='juniorguru', sort_rank=30)
    job2 = create_job('2', source='moo')  # noqa
    job3 = create_job('3', source='juniorguru', sort_rank=20)
    job4 = create_job('4', source='juniorguru', sort_rank=10)

    assert list(Job.newsletter_listing(3)) == [job1, job3, job4]


def test_newsletter_listing_backfills_with_other_sources(db_connection):
    job1 = create_job('1', source='moo', sort_rank=20)
    job2 = create_job('2', source='foo', sort_rank=10)
    job3 = create_job('3', source='bar', sort_rank=40)
    job4 = create_job('4', source='juniorguru', sort_rank=30)
    job5 = create_job('5', source='juniorguru', sort_rank=20)

    assert list(Job.newsletter_listing(5)) == [job4, job5, job3, job1, job2]


def test_newsletter_listing_backfills_up_to_min_count(db_connection):
    job1 = create_job('1', source='moo', sort_rank=5)
    job2 = create_job('2', source='foo', sort_rank=1)  # noqa
    job3 = create_job('3', source='bar', sort_rank=10)
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


@pytest.mark.parametrize('pricing_plan,expected', [
    ('community', False),
    ('standard', True),
    ('awesome-cool-hyper-super-plan', True),
])
def test_is_highlighted(pricing_plan, expected):
    job = Job(**prepare_job_data('1', pricing_plan=pricing_plan))

    assert job.is_highlighted is expected


@pytest.mark.parametrize('posted_at,expected', [
    (date(2020, 9, 25), False),
    (date(2020, 9, 26), True),
])
def test_tags_new(posted_at, expected):
    job = Job(**prepare_job_data('1', posted_at=posted_at))
    tags = job.tags(today=date(2020, 9, 28))

    assert ('NEW' in tags) is expected


@pytest.mark.parametrize('remote,expected', [
    (True, True),
    (False, False),
])
def test_tags_remote(remote, expected):
    job = Job(**prepare_job_data('1', remote=remote))
    tags = job.tags()

    assert ('REMOTE' in tags) is expected


@pytest.mark.parametrize('employment_types,expected', [
    # individual employment types
    (['FULL_TIME'], set()),
    (['PART_TIME'], {'PART_TIME'}),
    (['CONTRACT'], {'CONTRACT'}),
    (['PAID_INTERNSHIP'], {'INTERNSHIP'}),
    (['UNPAID_INTERNSHIP'], {'UNPAID_INTERNSHIP'}),
    (['INTERNSHIP'], {'INTERNSHIP'}),
    (['VOLUNTEERING'], {'VOLUNTEERING'}),

    # behavior together with full time
    (['FULL_TIME', 'PART_TIME'], {'ALSO_PART_TIME'}),
    (['FULL_TIME', 'CONTRACT'], {'ALSO_CONTRACT'}),
    (['FULL_TIME', 'PAID_INTERNSHIP'], {'ALSO_INTERNSHIP'}),
    (['FULL_TIME', 'UNPAID_INTERNSHIP'], {'ALSO_INTERNSHIP'}),
    (['FULL_TIME', 'INTERNSHIP'], {'ALSO_INTERNSHIP'}),
    (['FULL_TIME', 'VOLUNTEERING'], set()),

    # internship behavior
    (['PAID_INTERNSHIP', 'UNPAID_INTERNSHIP'], {'INTERNSHIP'}),
    (['INTERNSHIP', 'PAID_INTERNSHIP'], {'INTERNSHIP'}),
    (['INTERNSHIP', 'UNPAID_INTERNSHIP'], {'UNPAID_INTERNSHIP'}),

    # volunteering behavior
    (['VOLUNTEERING', 'FULL_TIME'], set()),
    (['VOLUNTEERING', 'PART_TIME'], {'PART_TIME'}),
    (['VOLUNTEERING', 'CONTRACT'], {'CONTRACT'}),
    (['VOLUNTEERING', 'PAID_INTERNSHIP'], {'INTERNSHIP'}),
    (['VOLUNTEERING', 'UNPAID_INTERNSHIP'], {'VOLUNTEERING', 'UNPAID_INTERNSHIP'}),
    (['VOLUNTEERING', 'INTERNSHIP'], {'INTERNSHIP'}),
    (['VOLUNTEERING'], {'VOLUNTEERING'}),
])
def test_tags_employment_types(employment_types, expected):
    job = Job(**prepare_job_data('1', employment_types=employment_types))
    tags = set(job.tags())

    assert expected == tags


@pytest.mark.parametrize('location_raw,location_place,region,expected', [
    # missing pieces
    (None, None, None, '?'),
    ('Brno, Česká republika', None, 'Brno', 'Brno, Česká republika'),
    ('Brno, Česká republika', 'Brno', None, 'Brno, Česká republika'),
    ('Brno, Česká republika', None, None, 'Brno, Česká republika'),

    # region
    ('Brno, Česká republika', 'Brno', 'Brno', 'Brno'),
    ('Káranice, Česká republika', 'Káranice', 'Hradec Králové', 'Káranice, Hradec Králové'),
    ('Berlin, Deutschland', 'Berlin', 'Německo', 'Berlin, Německo'),
])
def test_location(location_raw, location_place, region, expected):
    job = Job(**prepare_job_data('1',
                                 location_raw=location_raw,
                                 location_place=location_place,
                                 region=region))

    assert job.location == expected


@pytest.mark.parametrize('location_raw,remote,expected', [
    (None, True, 'na dálku'),
    (None, False, '?'),
    ('Brno', True, 'Brno, na dálku'),
    ('Brno', False, 'Brno'),
])
def test_location_with_remote(location_raw, remote, expected):
    job = Job(**prepare_job_data('1', location_raw=location_raw, remote=remote))

    assert job.location == expected
