import pytest

from jg.coop.lib import google_sheets


def get_range_notation():
    assert (
        google_sheets.get_range_notation(
            [
                ["Name", "", "", "Size"],
                ["a", "", "", "1"],
                ["b", "", "", "2"],
                ["c", "", "", "3"],
            ]
        )
        == "A1:D4"
    )


def get_range_notation_no_rows():
    with pytest.raises(ValueError):
        assert google_sheets.get_range_notation([])


def get_range_notation_no_cols():
    with pytest.raises(ValueError):
        assert google_sheets.get_range_notation([[], [], []])
