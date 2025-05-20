import pytest

from jg.coop.cli import screenshots


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://pyladies.cz", False),
        ("https://www.youtube.com/user/BBSobotka", False),
        ("https://www.youtube.com/@BronislavSobotka", False),
        ("https://www.youtube.com/channel/UC01guyOZpf40pUopBvdPwsg", False),
        ("https://www.youtube.com/watch?v=0v5K4GvK4Gs", True),
        ("https://youtu.be/0v5K4GvK4Gs", True),
    ],
)
def test_is_yt_screenshot(url, expected):
    assert screenshots.is_yt_screenshot((url, "... path ...")) is expected
