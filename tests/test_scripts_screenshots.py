import pytest

from scripts import screenshots


@pytest.mark.parametrize('url,expected', [
    ('https://example.com', 'https://example.com'),
    ('https://example.com/foo/', 'https://example.com/foo'),
    ('https://junior.guru/club/', 'http://localhost:5000/club'),
    ('https://junior.guru/learn/#english', 'http://localhost:5000/learn/#english'),
])
def test_parse_url(url, expected):
    assert screenshots.parse_url(url) == expected


def test_filter_yt_urls():
    assert screenshots.filter_yt_urls([
        'https://pyladies.cz',
        'https://pyvo.cz',
        'https://www.youtube.com/user/BBSobotka',
        'https://www.youtube.com/channel/UC01guyOZpf40pUopBvdPwsg',
        'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
        'https://youtu.be/0v5K4GvK4Gs',
    ]) == [
        'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
        'https://youtu.be/0v5K4GvK4Gs',
    ]


@pytest.mark.parametrize('url,expected', [
    ('https://www.youtube.com/watch?v=0v5K4GvK4Gs', '0v5K4GvK4Gs'),
    ('https://youtu.be/0v5K4GvK4Gs', '0v5K4GvK4Gs'),
    ('https://www.youtube.com/watch?v=3-wsqhCK-wU&list=PLhB6F20C-jTPITEXEHus6fVZDfNxzRbv_&index=5', '3-wsqhCK-wU'),
])
def test_parse_yt_id(url, expected):
    assert screenshots.parse_yt_id(url) == expected


def test_parse_yt_id_raises():
    with pytest.raises(ValueError):
        screenshots.parse_yt_id('https://junior.guru')
