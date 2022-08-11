import pytest

from juniorguru.utils import screenshots


@pytest.mark.parametrize('url,expected', [
    ('https://pyladies.cz', False),
    ('https://www.youtube.com/user/BBSobotka', False),
    ('https://www.youtube.com/channel/UC01guyOZpf40pUopBvdPwsg', False),
    ('https://www.youtube.com/watch?v=0v5K4GvK4Gs', True),
    ('https://youtu.be/0v5K4GvK4Gs', True),
])
def test_filter_yt_urls(url, expected):
    assert screenshots.is_yt_screenshot((url, '... path ...')) is expected


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
