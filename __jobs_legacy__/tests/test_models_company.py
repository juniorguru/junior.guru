from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models import Company, ClubUser


def create_company(id, **kwargs):
    return Company.create(id=id,
                          name=kwargs.get('name', 'Banana'),
                          filename=kwargs.get('filename', 'banana.svg'),
                          is_sponsoring_handbook=kwargs.get('is_sponsoring_handbook', False),
                          link=kwargs.get('link', 'https://banana.example.com'),
                          coupon_base=kwargs.get('coupon_base', 'BANANA123'),
                          student_coupon_base=kwargs.get('student_coupon_base'),
                          starts_at=kwargs.get('starts_at', date.today() - timedelta(days=10)),
                          expires_at=kwargs.get('expires_at', date.today() + timedelta(days=100)),
                          role_id=kwargs.get('role_id'),
                          student_role_id=kwargs.get('student_role_id'))


@pytest.fixture
def db_connection():
    models = [Company, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_listing_sorts_by_starting_date(db_connection):
    company1 = create_company('1', starts_at=date(2021, 4, 3))
    company2 = create_company('2', starts_at=date(2021, 4, 2))
    company3 = create_company('3', starts_at=date(2021, 4, 1))

    assert list(Company.listing()) == [company3, company2, company1]


def test_listing_sorts_by_name_if_starting_date_is_the_same(db_connection):
    company1 = create_company('1', name='Banana', starts_at=date(2021, 4, 1))
    company2 = create_company('2', name='Apricot', starts_at=date(2021, 4, 1))

    assert list(Company.listing()) == [company2, company1]


def test_listing_skips_expired(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1', starts_at=today, expires_at=date(2021, 4, 1))  # noqa
    company2 = create_company('2', starts_at=today, expires_at=date(2021, 5, 1))  # noqa
    company3 = create_company('3', starts_at=today, expires_at=date(2021, 5, 2))
    company4 = create_company('4', starts_at=today, expires_at=date(2021, 5, 3))

    assert set(Company.listing(today=today)) == {company3, company4}


def test_listing_includes_companies_without_expiration(db_connection):
    today = date(2021, 5, 1)
    company1 = create_company('1', starts_at=today, expires_at=date(2021, 5, 1))
    company2 = create_company('2', starts_at=today, expires_at=None)

    assert set(Company.listing(today=today)) == {company1, company2}


def test_listing_skips_planned(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1', starts_at=date(2021, 5, 1), expires_at=None)
    company2 = create_company('2', starts_at=date(2021, 5, 2), expires_at=None)
    company3 = create_company('3', starts_at=date(2021, 5, 3), expires_at=None)  # noqa
    company4 = create_company('4', starts_at=None, expires_at=None)  # noqa

    assert set(Company.listing(today=today)) == {company1, company2}


def test_handbook_listing(db_connection):
    company1 = create_company('1', is_sponsoring_handbook=True)
    company2 = create_company('2', is_sponsoring_handbook=False)  # noqa
    company3 = create_company('3', is_sponsoring_handbook=True)

    assert set(Company.handbook_listing()) == {company1, company3}


def test_students_listing(db_connection):
    company1 = create_company('1', student_coupon_base='STUDENT!')
    company2 = create_company('2', student_coupon_base=None)  # noqa
    company3 = create_company('3', student_coupon_base='STUDENT!')

    assert set(Company.students_listing()) == {company1, company3}


def test_list_employees(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@123>', coupon_base='XEROX')
    member2 = ClubUser.create(display_name='Bob', mention='<@123>', coupon_base='XEROX')
    member3 = ClubUser.create(display_name='Celine', mention='<@123>', coupon_base='ZALANDO')  # noqa
    company = create_company('1', coupon_base='XEROX')

    assert set(company.list_employees) == {member1, member2}


def test_list_students(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@123>', coupon_base='XEROXSTUDENT')
    member2 = ClubUser.create(display_name='Bob', mention='<@123>', coupon_base='XEROXSTUDENT')
    member3 = ClubUser.create(display_name='Celine', mention='<@123>', coupon_base='ZALANDOSTUDENT')  # noqa
    company = create_company('1', student_coupon_base='XEROXSTUDENT')

    assert set(company.list_students) == {member1, member2}

