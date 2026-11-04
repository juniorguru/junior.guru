from datetime import date

import pytest

from jg.coop.models.transaction import TransactionsCategory
from jg.coop.sync.transactions import (
    get_todo_key,
    normalize_variable_symbol,
)
from jg.coop.sync.transactions.categories_spec import pavlun


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

    assert get_todo_key(todo) == (date(2022, 2, 23), "444222", 6.0)


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


@pytest.mark.parametrize(
    "message, account_name",
    [
        ("pavlun", None),
        ("Adéla PAVLUN, faktura", None),
        ("rozhovor", "Pavlun Adéla"),
    ],
)
def test_pavlun(message: str, account_name: str | None):
    transaction = {"message": message, "account_name": account_name, "amount": -4000}

    assert pavlun(transaction, {}) == TransactionsCategory.PRODUCTION


def test_pavlun_ignores_incoming():
    transaction = {"message": "Pavlun", "account_name": None, "amount": 4000}

    assert pavlun(transaction, {}) is None
