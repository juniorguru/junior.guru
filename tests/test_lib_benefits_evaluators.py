from datetime import date

import pytest
from peewee import SqliteDatabase

from juniorguru.lib.benefits_evaluators import evaluate_members
from juniorguru.models.club import ClubUser
from juniorguru.models.partner import Partner, Partnership

from testing_utils import prepare_partner_data


@pytest.fixture
def db_connection():
    models = [Partner, Partnership, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


@pytest.mark.parametrize('members_count, expected', [
    (0, False),
    (1, True),
    (10, True),
])
def test_evaluate_members(db_connection, members_count, expected):
    partner = Partner.create(**prepare_partner_data(1))
    partnership = Partnership.create(partner=partner,
                                     starts_on=date(2023, 3, 16))
    for id in range(members_count):
        ClubUser.create(id=id,
                        display_name=f'Jane{id}',
                        mention=f'<@{id}>',
                        tag='...',
                        coupon=partner.coupon)

    assert evaluate_members(partnership) is expected
