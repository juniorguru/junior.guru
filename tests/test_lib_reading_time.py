import pytest

from juniorguru.lib.reading_time import reading_time


@pytest.mark.parametrize(
    "content_size, expected",
    [
        (None, 1),
        (0, 1),
        (20, 1),
        (5000, 4),
    ],
)
def test_calc_reading_time(content_size, expected):
    assert reading_time(content_size) == expected
