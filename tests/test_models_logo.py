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
                       link_re=kwargs.get('link_re', r'example\.com'),
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
