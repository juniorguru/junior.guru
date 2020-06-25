import pytest

from juniorguru.web import create_nav


def test_create_nav_active():
    tabs = [dict(endpoint='jobs', name='Find Jobs', name_short='Jobs'),
            dict(endpoint='cats', name='Find Cats', name_short='Cats')]

    assert create_nav(tabs, 'jobs') == dict(
        ordered=False,
        tabs=[dict(endpoint='jobs', name='Find Jobs', name_short='Jobs', active=True),
              dict(endpoint='cats', name='Find Cats', name_short='Cats', active=False)]
    )


def test_create_nav_active_error():
    tabs = [dict(endpoint='jobs', name='Find Jobs', name_short='Jobs'),
            dict(endpoint='cats', name='Find Cats', name_short='Cats')]

    with pytest.raises(ValueError):
        create_nav(tabs, 'index')


def test_create_nav_ordered():
    tabs = [dict(endpoint='jobs', name='Find Jobs', name_short='Jobs'),
            dict(endpoint='cats', name='Find Cats', name_short='Cats')]

    assert create_nav(tabs, 'jobs', ordered=True) == dict(
        ordered=True,
        tabs=[dict(endpoint='jobs', name='Find Jobs', name_short='Jobs', active=True, number=1),
              dict(endpoint='cats', name='Find Cats', name_short='Cats', active=False, number=2)]
    )
