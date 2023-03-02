from decimal import Decimal

import pytest

from juniorguru.sync.transactions import parse_todo_text


@pytest.mark.parametrize('text, expected', [
    ('Nespárovaná příchozí platba - VS: , částka: 3&nbsp;316,21 Kč STRIPE',
     dict(variable_symbol=None, amount=Decimal('3316.21'))),
    ('Nespárovaná příchozí platba - VS: 444222, částka: 644,00 Kč ',
     dict(variable_symbol='444222', amount=Decimal('644.00'))),
    ('Nespárovaná příchozí platba - VS: 1018620871, částka: 2&nbsp;619,42 Kč 1018620871206/RFB/1018620871206',
     dict(variable_symbol='1018620871', amount=Decimal('2619.42'))),
    ('Nespárovaná příchozí platba - VS: 0, částka: 4&nbsp;815,64 Kč STRIPE',
     dict(variable_symbol=None, amount=Decimal('4815.64'))),
])
def test_parse_todo_text(text, expected):
    assert parse_todo_text(text) == expected
