from datetime import date
import pytest
from peewee import SqliteDatabase

from juniorguru.models.course_provider import CourseProvider
from juniorguru.models.partner import Partner, Partnership, PartnershipPlan
from testing_utils import prepare_course_provider_data, prepare_partner_data


def create_course_provider(id, **kwargs):
    return CourseProvider.create(**prepare_course_provider_data(id, **kwargs))


def create_partner(id, **kwargs):
    return Partner.create(**prepare_partner_data(id, **kwargs))


@pytest.fixture
def db_connection():
    models = [CourseProvider, Partner, Partnership, PartnershipPlan]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


def test_listing_sorts_alphabetically(db_connection):
    course_provider1 = create_course_provider(1, name='Cool Courses')
    course_provider2 = create_course_provider(2, name='Awesome Courses')
    course_provider3 = create_course_provider(3, name='Wonderful Courses')

    assert list(CourseProvider.listing()) == [course_provider2, course_provider1, course_provider3]


def test_listing_sorts_alphabetically_case_insensitive(db_connection):
    course_provider1 = create_course_provider(1, name='Cool Courses')
    course_provider2 = create_course_provider(2, name='awesome Courses')
    course_provider3 = create_course_provider(3, name='Wonderful Courses')
    course_provider4 = create_course_provider(4, name='zzz Courses')

    assert list(CourseProvider.listing()) == [course_provider2, course_provider1, course_provider3, course_provider4]


def test_listing_sorts_partners_first(db_connection):
    today = date(2021, 5, 2)
    plan = PartnershipPlan.create(slug='plan', name='Plan', price=10000)
    partner = create_partner(1)
    Partnership.create(partner=partner, plan=plan, starts_on=today, expires_on=None)
    course_provider1 = create_course_provider(1, name='Cool Courses')
    course_provider2 = create_course_provider(2, name='Awesome Courses')
    course_provider3 = create_course_provider(3, name='Wonderful Courses', partner=partner)

    assert list(CourseProvider.listing(today=today)) == [course_provider3, course_provider2, course_provider1]


def test_listing_sorts_only_active_partners_first(db_connection):
    today = date(2021, 5, 2)
    plan = PartnershipPlan.create(slug='plan', name='Plan', price=10000)
    partner = create_partner(1)
    Partnership.create(partner=partner, plan=plan, starts_on=date(2021, 1, 1), expires_on=date(2021, 2, 1))
    course_provider1 = create_course_provider(1, name='Cool Courses')
    course_provider2 = create_course_provider(2, name='Awesome Courses')
    course_provider3 = create_course_provider(3, name='Wonderful Courses', partner=partner)

    assert list(CourseProvider.listing(today=today)) == [course_provider2, course_provider1, course_provider3]


def test_listing_sorts_partners_by_hierarchy_rank_then_by_name(db_connection):
    today = date(2021, 5, 2)
    plan1 = PartnershipPlan.create(slug='plan-top', name='Plan Top', price=10000)
    partner1 = create_partner(1)
    Partnership.create(partner=partner1, plan=plan1, starts_on=today, expires_on=None)
    plan2 = PartnershipPlan.create(slug='plan-basic', name='Plan Basic', price=100)
    partner2 = create_partner(2)
    Partnership.create(partner=partner2, plan=plan2, starts_on=today, expires_on=None)
    partner3 = create_partner(3)
    Partnership.create(partner=partner3, plan=plan2, starts_on=today, expires_on=None)
    course_provider1 = create_course_provider(1, name='Cool Courses', partner=partner2)
    course_provider2 = create_course_provider(2, name='Awesome Courses')
    course_provider3 = create_course_provider(3, name='Sexy Courses', partner=partner3)
    course_provider4 = create_course_provider(4, name='Wonderful Courses', partner=partner1)

    assert list(CourseProvider.listing(today=today)) == [course_provider4,  # top plan
                                                         course_provider1, course_provider3,  # basic plan
                                                         course_provider2]  # no plan
