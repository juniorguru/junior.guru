import pytest
from peewee import SqliteDatabase

from juniorguru.models.course_provider import CourseProvider


def create_course_provider(id, **kwargs):
    return CourseProvider.create(id=id,
                                 name=kwargs.pop('name', 'Test Course Provider'),
                                 slug=kwargs.pop('slug', f'test-course-provider-{id}'),
                                 url=kwargs.pop('url', 'https://example.com'),
                                 edit_url=kwargs.pop('edit_url', 'https://example.com/edit'),
                                 page_title=kwargs.pop('page_title', 'Test Course Provider'),
                                 page_description=kwargs.pop('page_description', 'Test Course Provider'),
                                 page_lead=kwargs.pop('page_lead', 'Test Course Provider'),
                                 **kwargs)


@pytest.fixture
def db_connection():
    models = [CourseProvider]
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
