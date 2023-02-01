from datetime import date

import pytest

from juniorguru.cli.students import subscription_to_row, to_csv
from juniorguru.models.partner import Partner, PartnerStudentSubscription


def test_to_csv():
    rows = [{'a': 1, 'b': 2, 'c': 3},
            {'a': None, 'b': 2, 'c': 3},
            {'a': 1, 'b': None, 'c': 3}]
    assert to_csv(rows) == (
        'a,b,c\r\n'
        '1,2,3\r\n'
        ',2,3\r\n'
        '1,,3\r\n'
    )


def test_to_csv_empty():
    rows = []
    with pytest.raises(ValueError):
        assert to_csv(rows)


def test_subscription_to_row():
    partner = Partner(name='Foo Corporation',
                      slug='foo',
                      logo_path='logos/foo.svg',
                      url='https://example.com')
    subscription = PartnerStudentSubscription(id='123',
                                              partner=partner,
                                              account_id='12345',
                                              name='Honza',
                                              email='honza@example.com',
                                              started_on=date.today(),
                                              invoiced_on=date.today())

    assert subscription_to_row(subscription) == dict(name='Honza',
                                                     email='honza@example.com',
                                                     started_on=date.today(),
                                                     invoiced_on=date.today())
