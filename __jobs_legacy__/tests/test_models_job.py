from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Job, JobMetric, JobDropped
from testing_utils import prepare_job_data


def create_job(id, **kwargs):
    return Job.create(**prepare_job_data(id, **kwargs))


@pytest.fixture
def db_connection():
    models = [JobMetric, Job, JobDropped]
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


def test_region_listing(db_connection):
    job1 = create_job('1', sort_rank=30,
                      locations=[dict(name='Brno', region='Brno')])
    job2 = create_job('2',  # noqa
                      locations=[dict(name='Praha', region='Praha')])
    job3 = create_job('3', sort_rank=20,
                      locations=[dict(name='Brno', region='Brno')])
    job4 = create_job('4', sort_rank=10,
                      locations=[dict(name='Brno', region='Brno')])

    assert list(Job.region_listing('Brno')) == [job1, job3, job4]


def test_remote_listing(db_connection):
    job1 = create_job('1', remote=True, sort_rank=30)
    job2 = create_job('2', remote=False)  # noqa
    job3 = create_job('3', remote=True, sort_rank=20)
    job4 = create_job('4', remote=True, sort_rank=10)

    assert list(Job.remote_listing()) == [job1, job3, job4]


def test_tags_listing(db_connection):
    job1 = create_job('1', employment_types=['FULL_TIME', 'PART_TIME', 'INTERNSHIP'], sort_rank=30)
    job2 = create_job('2', employment_types=['FULL_TIME', 'PART_TIME'], sort_rank=20)
    job3 = create_job('3', employment_types=['PART_TIME', 'PAID_INTERNSHIP'])  # noqa
    job4 = create_job('4', employment_types=['FULL_TIME', 'PART_TIME', 'UNPAID_INTERNSHIP'], sort_rank=10)

    assert list(Job.tags_listing(['ALSO_INTERNSHIP', 'ALSO_PART_TIME'])) == [job1, job2, job4]


def test_effective_link(db_connection):
    job = create_job('1', source='xyz', link='https://example.com/1234', apply_link=None)

    assert job.effective_link == 'https://example.com/1234'


def test_effective_link_apply(db_connection):
    job = create_job('1', source='xyz', link='https://example.com/1234', apply_link='https://example.com/1234?utm_something=123')

    assert job.effective_link == 'https://example.com/1234?utm_something=123'


def test_effective_link_juniorguru(db_connection):
    job = create_job('1', source='juniorguru', link='https://junior.guru/jobs/1234', apply_link='https://example.com/1234?utm_something=123')

    assert job.effective_link == 'https://junior.guru/jobs/1234'


def test_get_by_url(db_connection):
    job = create_job('1', link='https://example.com/1234', apply_link='https://example.com/1234?utm_something=123')

    assert Job.get_by_url('https://example.com/1234') == job


def test_get_by_url_raises_does_not_exist_error(db_connection):
    with pytest.raises(Job.DoesNotExist):
        Job.get_by_url('https://example.com/1234')


def test_get_by_url_apply(db_connection):
    job = create_job('1', link='https://example.com/1234', apply_link='https://example.com/1234?utm_something=123')

    assert Job.get_by_url('https://example.com/1234?utm_something=123') == job


def test_get_by_url_juniorguru(db_connection):
    job = create_job('1')

    assert Job.get_by_url('https://junior.guru/jobs/1/') == job


def test_get_by_url_juniorguru_raises_does_not_exist_error(db_connection):
    with pytest.raises(Job.DoesNotExist):
        Job.get_by_url('https://junior.guru/jobs/1/')


def test_juniorguru_get_by_id(db_connection):
    job = create_job('1', source='juniorguru')

    assert Job.juniorguru_get_by_id('1') == job


def test_juniorguru_get_by_id_raises_dost_not_exist_error(db_connection):
    create_job('1', source='remoteok')

    with pytest.raises(Job.DoesNotExist):
        assert Job.juniorguru_get_by_id('1')


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


def test_is_juniorguru_true():
    job = Job(**prepare_job_data('1', source='juniorguru'))

    assert job.is_juniorguru is True


def test_is_juniorguru_false():
    job = Job(**prepare_job_data('1', source='abcxyz'))

    assert job.is_juniorguru is False


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


@pytest.mark.parametrize('locations,expected', [
    # missing pieces
    ([], '?'),
    ([dict(name=None, region=None)], '?'),
    ([dict(name=None, region='Brno')], 'Brno'),
    ([dict(name='Brno', region=None)], 'Brno'),

    # region
    ([dict(name='Brno', region='Brno')], 'Brno'),
    ([dict(name='Káranice', region='Hradec Králové')], 'Káranice, Hradec Králové'),
    ([dict(name='Berlin', region='Německo')], 'Berlin, Německo'),

    # multiple
    ([dict(name='Brno', region='Brno'),
      dict(name='Káranice', region='Hradec Králové')], 'Brno, Káranice'),

    # too many
    ([dict(name='Brno', region='Brno'),
      dict(name='Praha', region='Praha'),
      dict(name='Káranice', region='Hradec Králové'),
      dict(name='Berlin', region='Německo')], 'Berlin, Brno…'),
])
def test_location(locations, expected):
    job = Job(**prepare_job_data('1', locations=locations))

    assert job.location == expected


@pytest.mark.parametrize('locations,remote,expected', [
    ([], True, 'na dálku'),
    ([], False, '?'),
    ([dict(name='Brno', region='Brno')], True, 'Brno, na dálku'),
    ([dict(name='Brno', region='Brno')], False, 'Brno'),
    ([dict(name='Brno', region='Brno'),
      dict(name='Praha', region='Praha')], True, 'Brno, Praha, na dálku'),
    ([dict(name='Brno', region='Brno'),
      dict(name='Praha', region='Praha'),
      dict(name='Liberec', region='Liberec')], True, 'Brno, Liberec a další, na dálku'),
])
def test_location_with_remote(locations, remote, expected):
    job = Job(**prepare_job_data('1', locations=locations, remote=remote))

    assert job.location == expected


def test_aggregate_metrics_jobs_count(db_connection):
    create_job('1')
    create_job('2')
    create_job('3')

    assert Job.aggregate_metrics()['jobs_count'] == 3


def test_aggregate_metrics_approved_jobs_count(db_connection):
    create_job('1', source='juniorguru')
    create_job('2', source='abc')
    create_job('3', source='xyz')

    assert Job.aggregate_metrics()['approved_jobs_count'] == 2


def test_aggregate_metrics_rejected_jobs_count(db_connection):
    JobDropped.create(source='juniorguru',
                      type='...', reason='...', response_url='...', item={})
    JobDropped.create(source='abc',
                      type='...', reason='...', response_url='...', item={})
    JobDropped.create(source='xyz',
                      type='...', reason='...', response_url='...', item={})

    assert Job.aggregate_metrics()['rejected_jobs_count'] == 2


def test_aggregate_metrics_companies_count(db_connection):
    create_job('1', company_link='https://example.com/1', source='juniorguru')
    create_job('2', company_link='https://example.com/2', source='juniorguru')
    create_job('3', company_link='https://example.com/2', source='juniorguru')
    create_job('4', company_link='https://example.com/3', source='xyz')

    assert Job.aggregate_metrics()['companies_count'] == 2


def test_aggregate_metrics_companies_count_past_jobs(db_connection):
    JobDropped.create(type='Expired',
                      item=dict(company_link='https://example.com/company1'),
                      reason='...', response_url='...', source='...')
    JobDropped.create(type='NotApproved',
                      item=dict(company_link='https://example.com/company2'),
                      reason='...', response_url='...', source='...')
    JobDropped.create(type='IrrelevantLanguage',
                      item=dict(company_link='https://example.com/company3'),
                      reason='...', response_url='...', source='...')

    assert Job.aggregate_metrics()['companies_count'] == 1


def test_aggregate_metrics_companies_count_past_jobs_unique(db_connection):
    JobDropped.create(type='Expired',
                      item=dict(company_link='https://example.com/company1'),
                      reason='...', response_url='...', source='...')
    JobDropped.create(type='Expired',
                      item=dict(company_link='https://example.com/company1'),
                      reason='...', response_url='...', source='...')

    assert Job.aggregate_metrics()['companies_count'] == 1


def test_aggregate_metrics_companies_count_past_and_present_jobs_unique(db_connection):
    create_job('1', company_link='https://example.com/company1', source='juniorguru')
    create_job('2', company_link='https://example.com/company2', source='juniorguru')
    create_job('3', company_link='https://example.com/company2', source='juniorguru')

    JobDropped.create(type='Expired',
                      item=dict(company_link='https://example.com/company1'),
                      reason='...', response_url='...', source='...')
    JobDropped.create(type='Expired',
                      item=dict(company_link='https://example.com/company3'),
                      reason='...', response_url='...', source='...')

    assert Job.aggregate_metrics()['companies_count'] == 3
