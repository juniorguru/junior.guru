from datetime import date

import pytest

from juniorguru.lib.discord_club import ClubChannelID, ClubEmoji, ClubMemberID
from juniorguru.models.base import SqliteDatabase
from juniorguru.models.club import ClubMessage, ClubUser
from juniorguru.models.partner import Partner, Partnership, PartnershipPlan
from juniorguru.sync.partners_intro import get_partners_without_intro

from testing_utils import prepare_partner_data


def create_intro(partner, created_at):
    author = ClubUser.create(id=ClubMemberID.BOT,
                             display_name='',
                             mention='',
                             tag='')
    return ClubMessage.create(id=123,
                              url='https://example.com',
                              content=f'{ClubEmoji.PARTNER_INTRO} {partner.name_markdown_bold}',
                              content_size=len(ClubEmoji.PARTNER_INTRO),
                              content_starting_emoji=ClubEmoji.PARTNER_INTRO,
                              created_at=created_at,
                              created_month='????-??',
                              author_is_bot=True,
                              channel_id=ClubChannelID.INTRO,
                              channel_name='',
                              author=author)

@pytest.fixture
def db_connection():
    models = [Partner, Partnership, PartnershipPlan, ClubMessage, ClubUser]
    db = SqliteDatabase(':memory:')
    with db:
        db.bind(models)
        db.create_tables(models)
        yield db
        db.drop_tables(models)


@pytest.fixture
def partner(db_connection):
    return Partner.create(**prepare_partner_data(1))


@pytest.fixture
def plan(db_connection):
    return PartnershipPlan.create(name='Basic', slug='basic', hierarchy_rank=1, price=100)


def test_get_partners_without_intro_yields_partner_without_intro(db_connection, partner, plan):
    today = date(2023, 4, 1)
    Partnership.create(partner=partner,
                       plan=plan,
                       starts_on=date(2023, 3, 1),
                       expires_on=date(2024, 3, 1))
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]


def test_get_partners_without_intro_skips_partner_with_intro(db_connection, partner, plan):
    today = date(2023, 4, 1)
    create_intro(partner, created_at=date(2023, 3, 15))
    Partnership.create(partner=partner,
                       plan=plan,
                       starts_on=date(2023, 3, 1),
                       expires_on=date(2024, 3, 1))
    partnerships = Partnership.active_listing(today=today)

    assert len(partnerships) == 1
    assert list(get_partners_without_intro(partnerships, today=today)) == []


def test_get_partners_without_intro_yields_partner_with_expired_intro(db_connection, partner, plan):
    today = date(2023, 5, 1)
    create_intro(partner, created_at=date(2023, 4, 30))
    Partnership.create(partner=partner,
                       plan=plan,
                       starts_on=date(2023, 5, 1),
                       expires_on=date(2024, 5, 1))
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]


def test_get_partners_without_intro_skips_barter_partner_with_recent_intro(db_connection, partner, plan):
    today = date(2023, 4, 1)
    create_intro(partner, created_at=date(2023, 3, 15))
    Partnership.create(partner=partner,
                       plan=plan,
                       starts_on=date(2023, 3, 1),
                       expires_on=None)
    partnerships = Partnership.active_listing(today=today)

    assert len(partnerships) == 1
    assert list(get_partners_without_intro(partnerships, today=today)) == []


def test_get_partners_without_intro_yields_barter_partner_with_expired_intro(db_connection, partner, plan):
    today = date(2023, 5, 1)
    create_intro(partner, created_at=date(2022, 3, 15))
    Partnership.create(partner=partner,
                       plan=plan,
                       starts_on=date(2023, 5, 1),
                       expires_on=None)
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]
