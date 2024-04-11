from datetime import date

import pytest

from project.sync.transactions import (
    get_todo_key,
    normalize_variable_symbol,
    parse_todo_text,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        (
            "Nespárovaná příchozí platba - VS: , částka: 3&nbsp;316,21 Kč STRIPE",
            dict(variable_symbol=None, amount=3316.21),
        ),
        (
            "Nespárovaná příchozí platba - VS: 444222, částka: 644,00 Kč ",
            dict(variable_symbol="444222", amount=644.00),
        ),
        (
            "Nespárovaná příchozí platba - VS: 1018620871, částka: 2&nbsp;619,42 Kč 1018620871206/RFB/1018620871206",
            dict(variable_symbol="1018620871", amount=2619.42),
        ),
        (
            "Nespárovaná příchozí platba - VS: 0, částka: 4&nbsp;815,64 Kč STRIPE",
            dict(variable_symbol="0", amount=4815.64),
        ),
    ],
)
def test_parse_todo_text(text, expected):
    assert parse_todo_text(text) == expected


def test_get_todo_key():
    todo = {
        "id": 3325647,
        "name": "invoice_payment_unpaired",
        "created_at": "2022-02-23T09:33:55.575+01:00",
        "completed_at": None,
        "invoice_id": None,
        "subject_id": None,
        "text": "Nespárovaná příchozí platba - VS: 444222, částka: 644,00 Kč ",
        "invoice_url": None,
        "subject_url": None,
    }

    assert get_todo_key(todo) == (date(2022, 2, 23), "444222", 644.0)


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, None),
        ("0", None),
        ("", None),
        ("123", "123"),
    ],
)
def test_normalize_variable_symbol(value, expected):
    assert normalize_variable_symbol(value) == expected
