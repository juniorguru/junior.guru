from datetime import date, timedelta

import pytest
from peewee import SqliteDatabase

from juniorguru.models.club import ClubUser
from juniorguru.models.company import Company, CompanyStudentSubscription


def create_company(id, **kwargs):
    return Company.create(id=id,
                          slug=kwargs.get('slug', f'banana{id}'),
                          name=kwargs.get('name', f'Banana #{id}'),
                          logo_filename=kwargs.get('logo_filename', 'banana.svg'),
                          is_sponsoring_handbook=kwargs.get('is_sponsoring_handbook', False),
                          url=kwargs.get('url', 'https://banana.example.com'),
                          coupon_base=kwargs.get('coupon_base', 'BANANA123'),
                          student_coupon_base=kwargs.get('student_coupon_base'),
                          starts_on=kwargs.get('starts_on', date.today() - timedelta(days=10)),
                          expires_on=kwargs.get('expires_on', date.today() + timedelta(days=100)),
                          role_id=kwargs.get('role_id'),
                          student_role_id=kwargs.get('student_role_id'))


def create_student_subscription(company, **kwargs):
    return CompanyStudentSubscription.create(company=company,
                                             memberful_id='123',
                                             name='Alice',
                                             email='alice@example.com',
                                             started_on=kwargs.get('started_on', date.today()),
                                             invoiced_on=kwargs.get('invoiced_on', date.today()))


@pytest.fixture
def db_connection():
    models = [Company, CompanyStudentSubscription, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_listing_sorts_by_starting_date(db_connection):
    company1 = create_company('1', starts_on=date(2021, 4, 3))
    company2 = create_company('2', starts_on=date(2021, 4, 2))
    company3 = create_company('3', starts_on=date(2021, 4, 1))

    assert list(Company.listing()) == [company3, company2, company1]


def test_listing_sorts_by_name_if_starting_date_is_the_same(db_connection):
    company1 = create_company('1', name='Banana', starts_on=date(2021, 4, 1))
    company2 = create_company('2', name='Apricot', starts_on=date(2021, 4, 1))

    assert list(Company.listing()) == [company2, company1]


def test_listing_skips_expired(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1', starts_on=today, expires_on=date(2021, 4, 1))  # noqa
    company2 = create_company('2', starts_on=today, expires_on=date(2021, 5, 1))  # noqa
    company3 = create_company('3', starts_on=today, expires_on=date(2021, 5, 2))
    company4 = create_company('4', starts_on=today, expires_on=date(2021, 5, 3))

    assert set(Company.listing(today=today)) == {company3, company4}


def test_listing_includes_companies_without_expiration(db_connection):
    today = date(2021, 5, 1)
    company1 = create_company('1', starts_on=today, expires_on=date(2021, 5, 1))
    company2 = create_company('2', starts_on=today, expires_on=None)

    assert set(Company.listing(today=today)) == {company1, company2}


def test_listing_skips_planned(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1', starts_on=date(2021, 5, 1), expires_on=None)
    company2 = create_company('2', starts_on=date(2021, 5, 2), expires_on=None)
    company3 = create_company('3', starts_on=date(2021, 5, 3), expires_on=None)  # noqa

    assert set(Company.listing(today=today)) == {company1, company2}


def test_handbook_listing(db_connection):
    company1 = create_company('1', is_sponsoring_handbook=True)
    company2 = create_company('2', is_sponsoring_handbook=False)  # noqa
    company3 = create_company('3', is_sponsoring_handbook=True)

    assert set(Company.handbook_listing()) == {company1, company3}


def test_schools_listing(db_connection):
    company1 = create_company('1', student_coupon_base='STUDENT!')
    company2 = create_company('2', student_coupon_base=None)  # noqa
    company3 = create_company('3', student_coupon_base='STUDENT!')

    assert set(Company.schools_listing()) == {company1, company3}


def test_list_members(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@123>', coupon_base='XEROX', tag='abc#1234')
    member2 = ClubUser.create(display_name='Bob', mention='<@123>', coupon_base='XEROX', tag='abc#1234')
    member3 = ClubUser.create(display_name='Celine', mention='<@123>', coupon_base='ZALANDO', tag='abc#1234')  # noqa
    company = create_company('1', coupon_base='XEROX')

    assert set(company.list_members) == {member1, member2}


def test_list_student_members(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@123>', coupon_base='XEROXSTUDENT', tag='abc#1234')
    member2 = ClubUser.create(display_name='Bob', mention='<@123>', coupon_base='XEROXSTUDENT', tag='abc#1234')
    member3 = ClubUser.create(display_name='Celine', mention='<@123>', coupon_base='ZALANDOSTUDENT', tag='abc#1234')  # noqa
    company = create_company('1', student_coupon_base='XEROXSTUDENT')

    assert set(company.list_student_members) == {member1, member2}


def test_get_by_slug(db_connection):
    create_company('1', slug='xerox')
    company = create_company('2', slug='zalando')

    assert Company.get_by_slug('zalando') == company


def test_get_by_slug_doesnt_exist(db_connection):
    create_company('1', slug='xerox')

    with pytest.raises(Company.DoesNotExist):
        assert Company.get_by_slug('zalando')


def test_get_by_slug_empty(db_connection):
    create_company('1', slug=None)

    with pytest.raises(ValueError):
        assert Company.get_by_slug(None)


def test_list_student_subscriptions(db_connection):
    company = create_company('1')
    subscription1 = create_student_subscription(company, invoiced_on=date.today())
    subscription2 = create_student_subscription(company, invoiced_on=None)

    assert set(company.list_student_subscriptions) == {subscription1, subscription2}


def test_list_student_subscriptions_billable(db_connection):
    company = create_company('1')
    subscription1 = create_student_subscription(company, invoiced_on=date.today())  # noqa
    subscription2 = create_student_subscription(company, invoiced_on=None)

    assert set(company.list_student_subscriptions_billable) == {subscription2}
