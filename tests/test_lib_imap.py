from datetime import date

import pytest

from jg.coop.lib.imap import format_imap_date


@pytest.mark.parametrize(
    "value, expected",
    [
        (date(2026, 11, 24), "24-Nov-2026"),
        (date(2026, 1, 5), "5-Jan-2026"),
    ],
)
def test_format_imap_date(value: date, expected: str):
    assert format_imap_date(value) == expected
