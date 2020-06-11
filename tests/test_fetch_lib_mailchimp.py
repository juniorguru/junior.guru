import hashlib
from datetime import date

import pytest

from juniorguru.fetch.lib import mailchimp


def test_get_collection():
    assert mailchimp.get_collection({
        '_links': [{'rel': 'self', 'href': 'https://api.example.com/things/'}],
        'things': [1, 2, 3, 4, 5],
        'total_items': 5,
    }, 'things') == [1, 2, 3, 4, 5]


def test_get_collection_raises():
    with pytest.raises(NotImplementedError) as excinfo:
        mailchimp.get_collection({
            '_links': [{'rel': 'self', 'href': 'https://api.example.com/things/'}],
            'things': [1, 2, 3, 4, 5],
            'total_items': 100,
        }, 'things')
    exc_message = str(excinfo.value).lower()

    assert 'pagination' in exc_message
    assert '5/100 things' in exc_message
    assert 'https://api.example.com/things/' in exc_message


def test_get_link():
    assert mailchimp.get_link({
        '_links': [
            {'rel': 'prev', 'href': 'https://api.example.com/things/?page=1'},
            {'rel': 'self', 'href': 'https://api.example.com/things/?page=2'},
            {'rel': 'next', 'href': 'https://api.example.com/things/?page=3'},
        ],
        'things': [1, 2, 3, 4, 5],
    }, 'next') == 'https://api.example.com/things/?page=3'


def test_sum_clicks_per_url():
    assert mailchimp.sum_clicks_per_url([
        {
            '_links': [...],
            'campaign_id': 'c8c3aec383',
            'click_percentage': 0.16666666666666666,
            'id': 'fc685ce42d',
            'last_click': '2019-12-11T21:15:44+00:00',
            'total_clicks': 3,
            'unique_click_percentage': 0.16666666666666666,
            'unique_clicks': 1,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            '_links': [...],
            'campaign_id': 'c8c3aec383',
            'click_percentage': 0.16666666666666666,
            'id': '75722a8bdf',
            'last_click': '2019-12-11T20:05:45+00:00',
            'total_clicks': 5,
            'unique_click_percentage': 0.16666666666666666,
            'unique_clicks': 2,
            'url': 'https://junior.guru/jobs/xyz2/'
        },
    ], 'total_clicks') == {
        'https://junior.guru/jobs/xyz1/': 3,
        'https://junior.guru/jobs/xyz2/': 5,
    }


def test_sum_clicks_per_url_sums_same_urls():
    assert mailchimp.sum_clicks_per_url([
        {
            'total_clicks': 3,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            'total_clicks': 2,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            'total_clicks': 3,
            'url': 'https://junior.guru/jobs/xyz2/'
        },
    ], 'total_clicks') == {
        'https://junior.guru/jobs/xyz1/': 5,
        'https://junior.guru/jobs/xyz2/': 3,
    }


def test_sum_clicks_per_url_filters_zeroes():
    assert mailchimp.sum_clicks_per_url([
        {
            'total_clicks': 0,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            'total_clicks': 2,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            'total_clicks': 0,
            'url': 'https://junior.guru/jobs/xyz2/'
        },
    ], 'total_clicks') == {
        'https://junior.guru/jobs/xyz1/': 2,
    }


def test_sum_clicks_per_external_url():
    assert mailchimp.sum_clicks_per_external_url([
        {
            'total_clicks': 3,
            'url': 'https://junior.guru/jobs/xyz1/'
        },
        {
            'total_clicks': 2,
            'url': 'https://example.com/jobs/abc/'
        },
        {
            'total_clicks': 3,
            'url': 'https://example.com/jobs/abc1/'
        },
    ], 'total_clicks') == {
        'https://example.com/jobs/abc/': 2,
        'https://example.com/jobs/abc1/': 3,
    }


@pytest.mark.parametrize('url,expected', [
    ('https://junior.guru', False),
    ('http://junior.guru', False),
    ('https://junior.guru/jobs/xyz1/', False),
    ('https://example.com', True),
    ('http://example.com', True),
    ('https://example.com/jobs/', True),
])
def test_is_external_url(url, expected):
    assert mailchimp.is_external_url(url) is expected
