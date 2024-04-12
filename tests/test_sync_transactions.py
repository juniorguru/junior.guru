from datetime import date

import pytest

from jg.coop.sync.transactions import (
    get_todo_key,
    normalize_variable_symbol,
)


def test_get_todo_key():
    todo = {
        "id": 3325647,
        "name": "invoice_payment_unpaired",
        "created_at": "2022-02-23T09:33:55.575+01:00",
        "completed_at": None,
        "text": "Nespárovaná příchozí platba - VS: 444222, částka: 6,00 Kč at se dari",
        "related_objects": [],
        "params": {
            "amount": "6.0",
            "bank_account_id": "9862",
            "bank_account_name": "Bankovní účet",
            "counterparty_bank_account_number": "1027672020/3030",
            "currency": "CZK",
            "note": "at se dari",
            "variable_symbol": "444222",
        },
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
