import pytest

from juniorguru.fetch.lib import google_sheets


def test_records_to_rows():
    assert google_sheets.records_to_rows([
        {'name': 'Anča', 'size': 42},
        {'name': 'Bob', 'size': 2, 'flag': 'no'},
        {'name': 'Zuzejk', 'size': 400},
        {'name': 'David', 'size': 4, 'flag': 'yes'},
    ]) == [
        ['name', 'size', 'flag'],
        ['Anča', 42, None],
        ['Bob', 2, 'no'],
        ['Zuzejk', 400, None],
        ['David', 4, 'yes'],
    ]


def get_range_notation():
    assert google_sheets.get_range_notation([
        ['Name', '', '', 'Size'],
        ['a', '', '', '1'],
        ['b', '', '', '2'],
        ['c', '', '', '3'],
    ]) == 'A1:D4'


def get_range_notation_no_rows():
    with pytest.raises(ValueError):
        assert google_sheets.get_range_notation([])


def get_range_notation_no_cols():
    with pytest.raises(ValueError):
        assert google_sheets.get_range_notation([[], [], []])
