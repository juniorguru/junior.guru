import uuid
from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.models.club import ClubUser
from juniorguru.models.company import (Company, CompanyStudentSubscription, Partnership,
                                       PartnershipBenefit, PartnershipPlan)


def create_company(id, **kwargs):
    return Company.create(id=id,
                          slug=kwargs.get('slug', f'banana{id}'),
                          name=kwargs.get('name', f'Banana #{id}'),
                          logo_path=kwargs.get('logo_path', 'logos/banana.svg'),
                          url=kwargs.get('url', 'https://banana.example.com'),
                          coupon=kwargs.get('coupon', 'BANANA123123123'),
                          student_coupon=kwargs.get('student_coupon'),
                          role_id=kwargs.get('role_id'),
                          student_role_id=kwargs.get('student_role_id'))


def create_plan(slug, benefit_slugs=None):
    plan = PartnershipPlan.create(slug=slug,
                                  name=f"Plan '{slug}'",
                                  price=10000)
    for position, benefit_slug in enumerate(benefit_slugs or []):
        PartnershipBenefit.create(position=position,
                                  text=f"Benefit '{benefit_slug}'",
                                  icon='beer',
                                  plan=plan,
                                  slug=benefit_slug)
    return plan


def create_partnership(partner, starts_on, expires_on, plan=None):
    return Partnership.create(partner=partner,
                              plan=plan or create_plan(f'basic-{uuid.uuid4()}'),
                              starts_on=starts_on,
                              expires_on=expires_on)


def create_student_subscription(company, **kwargs):
    return CompanyStudentSubscription.create(company=company,
                                             account_id='123',
                                             name='Alice',
                                             email='alice@example.com',
                                             started_on=kwargs.get('started_on', date.today()),
                                             invoiced_on=kwargs.get('invoiced_on', date.today()))


@pytest.fixture
def db_connection():
    models = [ClubUser, Company, CompanyStudentSubscription,
              Partnership, PartnershipPlan, PartnershipBenefit]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


@pytest.fixture
def plan_basic():
    return create_plan('basic', ['food', 'drinks'])


@pytest.fixture
def plan_top():
    return create_plan('top', ['flowers', 'balloon'])


@pytest.fixture
def plan_handbook():
    return create_plan('handbook', ['logo_handbook', 'flowers', 'balloon'])


def test_company_active_partnership(db_connection):
    today = date(2021, 5, 2)
    company = create_company('1')
    partnership1 = create_partnership(company, date(2020, 12, 1), date(2021, 1, 1))  # noqa
    partnership2 = create_partnership(company, date(2021, 4, 1), None)

    assert company.active_partnership(today=today) == partnership2


def test_company_active_partnership_no_active_partnership(db_connection):
    today = date(2021, 5, 2)
    company = create_company('1')
    create_partnership(company, date(2020, 12, 1), date(2021, 1, 1))
    create_partnership(company, date(2021, 4, 1), date(2021, 4, 15))

    assert company.active_partnership(today=today) is None


def test_company_active_partnership_no_partnership(db_connection):
    company = create_company('1')

    assert company.active_partnership() is None


def test_company_active_listing(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1')
    create_partnership(company1, today, date(2021, 4, 1))
    company2 = create_company('2')
    create_partnership(company2, today, date(2021, 5, 1))
    company3 = create_company('3')
    create_partnership(company3, today, date(2021, 5, 2))
    company4 = create_company('4')
    create_partnership(company4, today, date(2021, 5, 3))

    assert set(Company.active_listing(today=today)) == {company3, company4}


def test_company_active_listing_with_barters(db_connection):
    today = date(2021, 5, 1)
    company1 = create_company('1')
    create_partnership(company1, today, date(2021, 5, 1))
    company2 = create_company('2')
    create_partnership(company2, today, None)

    assert set(Company.active_listing(today=today)) == {company1, company2}


def test_company_active_listing_without_barters(db_connection):
    today = date(2021, 5, 1)
    company1 = create_company('1')
    create_partnership(company1, today, date(2021, 5, 1))
    company2 = create_company('2')
    create_partnership(company2, today, None)

    assert set(Company.active_listing(today=today, include_barters=False)) == {company1}


def test_company_active_listing_skips_planned(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1')
    create_partnership(company1, date(2021, 5, 1), None)
    company2 = create_company('2')
    create_partnership(company2, date(2021, 5, 2), None)
    company3 = create_company('3')
    create_partnership(company3, date(2021, 5, 3), None)

    assert set(Company.active_listing(today=today)) == {company1, company2}


def test_company_active_listing_sorts_by_name(db_connection):
    today = date(2021, 5, 2)
    company1 = create_company('1', name='Company B')
    create_partnership(company1, date(2021, 4, 1), None)
    company2 = create_company('2', name='Company C')
    create_partnership(company2, date(2021, 4, 2), None)
    company3 = create_company('3', name='Company A')
    create_partnership(company3, date(2021, 4, 3), None)

    assert list(Company.active_listing(today=today)) == [company3, company1, company2]


def test_company_active_listing_with_multiple_partnerships(db_connection):
    today = date(2023, 6, 1)
    company1 = create_company('1')
    create_partnership(company1, date(2023, 2, 1), date(2023, 5, 1))
    create_partnership(company1, date(2023, 5, 15), None)

    assert list(Company.active_listing(today=today)) == [company1]


def test_company_expired_listing(db_connection):
    today = date(2023, 5, 2)
    company1 = create_company('1')
    create_partnership(company1, date(2023, 3, 1), date(2023, 4, 1))
    company2 = create_company('2')
    create_partnership(company2, date(2023, 3, 1), date(2023, 5, 1))
    company3 = create_company('3')
    create_partnership(company3, date(2023, 3, 1), date(2023, 5, 2))
    company4 = create_company('4')
    create_partnership(company4, date(2023, 3, 1), date(2023, 5, 3))

    assert set(Company.expired_listing(today=today)) == {company1, company2}


def test_company_expired_listing_skips_companies_without_expiration(db_connection):
    today = date(2023, 5, 1)
    company1 = create_company('1')
    create_partnership(company1, date(2023, 3, 1), date(2023, 4, 1))
    company2 = create_company('2')
    create_partnership(company2, date(2023, 3, 1), None)

    assert set(Company.expired_listing(today=today)) == {company1}


def test_company_expired_listing_skips_planned(db_connection):
    today = date(2023, 5, 1)
    company1 = create_company('1')
    create_partnership(company1, date(2023, 2, 1), date(2023, 4, 1))
    company2 = create_company('2')
    create_partnership(company2, date(2023, 3, 1), date(2023, 4, 1))
    company3 = create_company('3')
    create_partnership(company3, date(2023, 6, 1), date(2023, 7, 1))

    assert set(Company.expired_listing(today=today)) == {company1, company2}


def test_company_expired_listing_sorts_by_expiration_date_then_by_name(db_connection):
    today = date(2023, 6, 1)
    company1 = create_company('1', name='Company B')
    create_partnership(company1, date(2023, 2, 1), date(2023, 5, 1))
    company2 = create_company('2', name='Company XYZ')
    create_partnership(company2, date(2023, 3, 1), date(2023, 4, 1))
    company3 = create_company('3', name='Company A')
    create_partnership(company3, date(2023, 2, 1), date(2023, 5, 1))

    assert list(Company.expired_listing(today=today)) == [company3, company1, company2]


def test_company_expired_listing_skips_active_partners(db_connection):
    today = date(2023, 6, 1)
    company1 = create_company('1')
    create_partnership(company1, date(2023, 2, 1), date(2023, 5, 1))
    create_partnership(company1, date(2023, 5, 15), None)

    assert list(Company.expired_listing(today=today)) == []


def test_company_handbook_listing(db_connection, plan_basic, plan_handbook):
    company1 = create_company('1')
    create_partnership(company1, date(2023, 1, 1), None, plan=plan_basic)
    company2 = create_company('2')
    create_partnership(company2, date(2023, 1, 1), None, plan=plan_handbook)
    company3 = create_company('3')
    create_partnership(company3, date(2023, 1, 1), None, plan=plan_basic)

    assert list(Company.handbook_listing()) == [company2]


def test_company_handbook_listing_sorts_by_name(db_connection, plan_handbook):
    company1 = create_company('1', name='Orange')
    create_partnership(company1, date(2023, 1, 1), None, plan=plan_handbook)
    company2 = create_company('2', name='Banana')
    create_partnership(company2, date(2023, 1, 1), None, plan=plan_handbook)
    company3 = create_company('3', name='Apple')
    create_partnership(company3, date(2023, 1, 1), None, plan=plan_handbook)

    assert list(Company.handbook_listing()) == [company3, company2, company1]


def test_company_schools_listing(db_connection):
    company1 = create_company('1', student_coupon='STUDENT!')
    company2 = create_company('2', student_coupon=None)  # noqa
    company3 = create_company('3', student_coupon='STUDENT!')

    assert set(Company.schools_listing()) == {company1, company3}


def test_company_schools_listing_sorts_by_name(db_connection):
    company1 = create_company('1', name='Banana', student_coupon='STUDENT!')
    company2 = create_company('3', name='Apple', student_coupon='STUDENT!')

    assert list(Company.schools_listing()) == [company2, company1]


def test_company_active_schools_listing(db_connection):
    today = date(2023, 6, 1)
    company1 = create_company('1', student_coupon='STUDENT!')
    create_partnership(company1, date(2023, 1, 1), None)
    company2 = create_company('2', student_coupon=None)
    create_partnership(company2, date(2023, 1, 1), None)
    company3 = create_company('3', student_coupon='STUDENT!')
    create_partnership(company3, date(2023, 1, 1), date(2023, 5, 1))

    assert [Company.active_schools_listing(today=today)] == [company1]


def test_company_list_members(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@111>', coupon='XEROX', tag='abc#1234')
    member2 = ClubUser.create(display_name='Bob', mention='<@222>', coupon='XEROX', tag='abc#1234')
    member3 = ClubUser.create(display_name='Celine', mention='<@333>', coupon='ZALANDO', tag='abc#1234')  # noqa
    company = create_company('1', coupon='XEROX')

    assert set(company.list_members) == {member1, member2}


def test_company_list_student_members(db_connection):
    member1 = ClubUser.create(display_name='Alice', mention='<@111>', coupon='XEROXSTUDENT', tag='abc#1234')
    member2 = ClubUser.create(display_name='Bob', mention='<@222>', coupon='XEROXSTUDENT', tag='abc#1234')
    member3 = ClubUser.create(display_name='Celine', mention='<@333>', coupon='ZALANDOSTUDENT', tag='abc#1234')  # noqa
    company = create_company('1', student_coupon='XEROXSTUDENT')

    assert set(company.list_student_members) == {member1, member2}


def test_company_get_by_slug(db_connection):
    create_company('1', slug='xerox')
    company = create_company('2', slug='zalando')

    assert Company.get_by_slug('zalando') == company


def test_company_get_by_slug_doesnt_exist(db_connection):
    create_company('1', slug='xerox')

    with pytest.raises(Company.DoesNotExist):
        assert Company.get_by_slug('zalando')


def test_company_list_student_subscriptions(db_connection):
    company = create_company('1')
    subscription1 = create_student_subscription(company, invoiced_on=date.today())
    subscription2 = create_student_subscription(company, invoiced_on=None)

    assert set(company.list_student_subscriptions) == {subscription1, subscription2}


def test_company_list_student_subscriptions_billable(db_connection):
    company = create_company('1')
    subscription1 = create_student_subscription(company, invoiced_on=date.today())  # noqa
    subscription2 = create_student_subscription(company, invoiced_on=None)

    assert set(company.list_student_subscriptions_billable) == {subscription2}


def test_plan_get_by_slug(db_connection):
    create_plan('top')
    plan = create_plan('basic')

    assert PartnershipPlan.get_by_slug('basic') == plan


def test_plan_get_by_slug_doesnt_exist(db_connection):
    create_plan('top')

    with pytest.raises(PartnershipPlan.DoesNotExist):
        assert PartnershipPlan.get_by_slug('basic')


def test_plan_hierarchy(db_connection, plan_basic, plan_top):
    plan_top.includes = plan_basic
    plan_top.save()

    assert list(plan_top.hierarchy) == [plan_basic, plan_top]


def test_plan_weight(db_connection, plan_basic, plan_top):
    plan_top.includes = plan_basic
    plan_top.save()

    assert (plan_basic.weight, plan_top.weight) == (0, 1)


def test_plan_benefits_all(db_connection, plan_basic, plan_top):
    plan_top.includes = plan_basic
    plan_top.save()

    assert [benefit.slug for benefit in plan_top.benefits()] == ['food', 'drinks', 'flowers', 'balloon']



def test_plan_benefits_own(db_connection, plan_basic, plan_top):
    plan_top.includes = plan_basic
    plan_top.save()

    assert [benefit.slug for benefit in plan_top.benefits(all=False)] == ['flowers', 'balloon']
