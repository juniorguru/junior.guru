from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Logo, LogoMetric


def create_logo(_id, **kwargs):
    t = date.today()
    return Logo.create(id=_id,
                       name=kwargs.get('name', 'Awesome Company'),
                       filename=kwargs.get('filename', 'awesome-company.svg'),
                       email=kwargs.get('email', 'recruitment@example.com'),
                       link=kwargs.get('link', 'https://jobs.example.com'),
                       link_re=kwargs.get('link_re'),
                       months=kwargs.get('monhts', 12),
                       starts_at=kwargs.get('starts_at', t),
                       expires_at=kwargs.get('expires_at', t + timedelta(days=365)))


@pytest.fixture
def db_connection():
    models = [LogoMetric, Logo]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_listing_sort_by_months(db_connection):
    logo1 = create_logo('1', months=12)
    logo2 = create_logo('2', months=3)
    logo3 = create_logo('3', months=6)

    assert Logo.listing() == [logo1, logo3, logo2]


def test_listing_sort_by_starts_at(db_connection):
    t = date.today()
    logo1 = create_logo('1', months=12, starts_at=t - timedelta(days=6))
    logo2 = create_logo('2', months=12, starts_at=t - timedelta(days=1))
    logo3 = create_logo('3', months=12, starts_at=t - timedelta(days=3))

    assert Logo.listing() == [logo1, logo3, logo2]


def test_listing_only_active(db_connection):
    t = date.today()
    logo1 = create_logo('1', starts_at=t, expires_at=t + timedelta(days=30))
    logo2 = create_logo('2', starts_at=t - timedelta(days=30), expires_at=t)
    create_logo('3', starts_at=t - timedelta(days=30), expires_at=t - timedelta(days=1))
    create_logo('4', starts_at=t + timedelta(days=1), expires_at=t + timedelta(days=30))
    logo5 = create_logo('5', starts_at=t - timedelta(days=30), expires_at=t + timedelta(days=30))

    assert set(Logo.listing(today=t)) == {logo1, logo2, logo5}


def test_get_by_url(db_connection):
    logo1 = create_logo('1', link='https://abc.example.com')
    logo2 = create_logo('2', link='https://xyz.example.com')

    assert Logo.get_by_url('https://abc.example.com/something/') == logo1
    assert Logo.get_by_url('https://xyz.example.com/moo/?utm_medium=foo') == logo2


def test_get_by_url_explicit_re(db_connection):
    logo1 = create_logo('1', link='https://abc.example.com', link_re=r'abc\.example\.com|moo\.example\.com')
    logo2 = create_logo('2', link='https://xyz.example.com', link_re=r'xyz\.example\.com|utm_medium')

    assert Logo.get_by_url('https://abc.example.com/something/') == logo1
    assert Logo.get_by_url('https://moo.example.com/everything/?v=123') == logo1
    assert Logo.get_by_url('https://xyz.example.com/moo/') == logo2
    assert Logo.get_by_url('https://example.com/moo/?utm_medium=foo') == logo2


def test_get_by_url_no_match(db_connection):
    create_logo('1', link='https://abc.example.com')
    create_logo('2', link='https://xyz.example.com')

    with pytest.raises(Logo.DoesNotExist):
        Logo.get_by_url('https://example.com/moo/?utm_medium=foo')


def test_get_by_url_multiple_match(db_connection):
    create_logo('1', link='https://example.com', link_re=r'example\.com')
    create_logo('2', link='https://example.com/something/', link_re=r'example\.com')

    with pytest.raises(Logo.AmbiguousMatch):
        Logo.get_by_url('https://example.com/moo/')


def test_days_since_started(db_connection):
    logo = create_logo('1', starts_at=date(1987, 8, 30))

    assert logo.days_since_started(today=date(1987, 9, 8)) == 9


def test_days_until_expires(db_connection):
    logo = create_logo('1', expires_at=date(1987, 9, 8))

    assert logo.days_until_expires(today=date(1987, 8, 30)) == 9


@pytest.mark.parametrize('today,expected', [
    pytest.param(date(2020, 5, 20), False, id='not soon'),
    pytest.param(date(2020, 5, 26), False, id='36 days before'),
    pytest.param(date(2020, 5, 27), True, id='35 days before'),
    pytest.param(date(2020, 6, 1), True, id='30 days before'),
    pytest.param(date(2020, 6, 30), True, id='day before'),
    pytest.param(date(2020, 7, 1), True, id='the same day'),
])
def test_expires_soon(db_connection, today, expected):
    logo = create_logo('1', starts_at=date(2020, 1, 1), expires_at=date(2020, 7, 1))

    assert logo.expires_soon(today=today) is expected


def test_from_values_per_date(db_connection):
    logo = create_logo('1', starts_at=date(2020, 9, 1), expires_at=date(2020, 10, 1))
    metric = LogoMetric.from_values_per_date(logo, 'users', {
        date(2020, 8, 15): 1000,
        date(2020, 9, 1): 10,
        date(2020, 9, 15): 20,
        date(2020, 10, 1): 30,
        date(2020, 10, 15): 1000,
    })

    assert metric.logo == logo
    assert metric.name == 'users'
    assert metric.value == 10 + 20 + 30
