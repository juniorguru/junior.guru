from datetime import date

import pytest

from jg.core.lib.discord_club import ClubChannelID, ClubEmoji, ClubMemberID
from jg.core.models.club import ClubMessage, ClubUser
from jg.core.models.partner import Partner, Partnership, PartnershipPlan
from jg.core.sync.partners_intro import get_partners_without_intro

from testing_utils import prepare_partner_data, prepare_test_db


def create_intro(partner, created_at):
    author = ClubUser.create(id=ClubMemberID.BOT, display_name="", mention="")
    return ClubMessage.create(
        id=123,
        url="https://example.com",
        content=f"{ClubEmoji.PARTNER_INTRO} {partner.name_markdown_bold}",
        content_size=len(ClubEmoji.PARTNER_INTRO),
        content_starting_emoji=ClubEmoji.PARTNER_INTRO,
        created_at=created_at,
        created_month="????-??",
        author_is_bot=True,
        channel_id=ClubChannelID.INTRO,
        channel_name="",
        parent_channel_id=ClubChannelID.INTRO,
        parent_channel_name="",
        author=author,
    )


@pytest.fixture
def test_db():
    yield from prepare_test_db(
        [Partner, Partnership, PartnershipPlan, ClubMessage, ClubUser]
    )


@pytest.fixture
def partner(test_db):
    return Partner.create(**prepare_partner_data(1))


@pytest.fixture
def plan(test_db):
    return PartnershipPlan.create(
        name="Basic", slug="basic", hierarchy_rank=1, price=100
    )


def test_get_partners_without_intro_yields_partner_without_intro(
    test_db, partner, plan
):
    today = date(2023, 4, 1)
    Partnership.create(
        partner=partner,
        plan=plan,
        starts_on=date(2023, 3, 1),
        expires_on=date(2024, 3, 1),
    )
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]


def test_get_partners_without_intro_skips_partner_with_intro(test_db, partner, plan):
    today = date(2023, 4, 1)
    create_intro(partner, created_at=date(2023, 3, 15))
    Partnership.create(
        partner=partner,
        plan=plan,
        starts_on=date(2023, 3, 1),
        expires_on=date(2024, 3, 1),
    )
    partnerships = Partnership.active_listing(today=today)

    assert len(partnerships) == 1
    assert list(get_partners_without_intro(partnerships, today=today)) == []


def test_get_partners_without_intro_yields_partner_with_expired_intro(
    test_db, partner, plan
):
    today = date(2023, 5, 1)
    create_intro(partner, created_at=date(2023, 4, 30))
    Partnership.create(
        partner=partner,
        plan=plan,
        starts_on=date(2023, 5, 1),
        expires_on=date(2024, 5, 1),
    )
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]


def test_get_partners_without_intro_skips_barter_partner_with_recent_intro(
    test_db, partner, plan
):
    today = date(2023, 4, 1)
    create_intro(partner, created_at=date(2023, 3, 15))
    Partnership.create(
        partner=partner, plan=plan, starts_on=date(2023, 3, 1), expires_on=None
    )
    partnerships = Partnership.active_listing(today=today)

    assert len(partnerships) == 1
    assert list(get_partners_without_intro(partnerships, today=today)) == []


def test_get_partners_without_intro_yields_barter_partner_with_expired_intro(
    test_db, partner, plan
):
    today = date(2023, 5, 1)
    create_intro(partner, created_at=date(2022, 3, 15))
    Partnership.create(
        partner=partner, plan=plan, starts_on=date(2023, 5, 1), expires_on=None
    )
    partnerships = Partnership.active_listing(today=today)

    assert list(get_partners_without_intro(partnerships, today=today)) == [partner]
