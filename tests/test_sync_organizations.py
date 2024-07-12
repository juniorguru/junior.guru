from datetime import date

import pytest

from jg.coop.sync.organizations import (
    PlanEntity,
    get_renews_on,
    get_start_on,
    next_month,
    parse_note,
    parse_plan_id,
    parse_subscription_id,
    parse_tier_name,
    prepare_tiers,
)


@pytest.fixture
def admin_base_url() -> str:
    return "https://juniorguru.memberful.com"


@pytest.mark.parametrize(
    "periods, today, expected",
    [
        pytest.param(
            [["2021-02", None]],
            date(2024, 6, 1),
            date(2025, 3, 1),
            id="no end, start before this month",
        ),
        pytest.param(
            [["2021-07", None]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="no end, start after this month",
        ),
        pytest.param(
            [["2021-06", None]],
            date(2024, 6, 1),
            date(2025, 7, 1),
            id="no end, start this month",
        ),
        pytest.param(
            [["2021-02", "2024-02"]],
            date(2024, 6, 1),
            None,
            id="past",
        ),
        pytest.param(
            [["2021-07", "2024-07"]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="future",
        ),
        pytest.param(
            [["2021-07", "2028-07"]],
            date(2024, 6, 1),
            date(2028, 8, 1),
            id="far future",
        ),
        pytest.param(
            [["2021-02", "2024-07"]],
            date(2024, 6, 1),
            date(2024, 8, 1),
            id="different starting and renew months",
        ),
        pytest.param(
            [["1999-02", "2001-02"], ["2021-02", None]],
            date(2024, 6, 1),
            date(2025, 3, 1),
            id="skips past periods",
        ),
    ],
)
def test_get_renews_on(
    periods: list[tuple[str, str | None]], today: date, expected: date
):
    assert get_renews_on(periods, today) == expected


@pytest.mark.parametrize(
    "periods, expected",
    [
        ([["2021-02", None]], date(2021, 2, 1)),
        ([["2021-02", None], ["1999-02", "2001-02"]], date(1999, 2, 1)),
    ],
)
def test_get_start_on(periods: list[tuple[str, str | None]], expected: date):
    assert get_start_on(periods) == expected


@pytest.mark.parametrize(
    "note, expected",
    [
        (" něco něco ", "něco něco"),
        ("", None),
        ("\t\t\t", None),
        (None, None),
    ],
)
def test_parse_note(note: str | None, expected: str | None):
    assert parse_note(note) == expected


@pytest.mark.parametrize(
    "name",
    [
        "Roční členství v klubu",
        "Mentoring „CoreSkill“",
        "Klubové lekce angličtiny",
    ],
)
def test_parse_tier_name_raises(name: str):
    with pytest.raises(ValueError):
        parse_tier_name(name)


def test_next_month():
    assert next_month(date(2024, 12, 6)) == date(2025, 1, 1)


def test_parse_plan_id(admin_base_url: str):
    assert parse_plan_id(f"{admin_base_url}/admin/plans/111101/") == 111101


def test_parse_plan_id_raises():
    with pytest.raises(ValueError):
        parse_plan_id("https://example.com/admin/plans/111101")


def test_parse_subscription_id(admin_base_url: str):
    assert (
        parse_subscription_id(f"{admin_base_url}/admin/subscriptions/3699651/")
        == 3699651
    )


def test_parse_subscription_id_raises():
    with pytest.raises(ValueError):
        parse_subscription_id("https://example.com/admin/subscriptions/3699651")


def test_prepare_tiers():
    plans = [
        PlanEntity(
            id="333",
            name="Tarif „Voníme“",
            forSale=True,
            priceCents=300,
            additionalMemberPriceCents=300,
        ),
        PlanEntity(
            id="111",
            name="Tarif „Prdíme“",
            forSale=True,
            priceCents=100,
            additionalMemberPriceCents=0,
        ),
        PlanEntity(
            id="222",
            name="Tarif „Smrdíme“",
            forSale=True,
            priceCents=200,
            additionalMemberPriceCents=200,
        ),
    ]

    assert prepare_tiers(plans) == [
        dict(priority=0, plan_id=111, name="Prdíme", price=1, member_price=None),
        dict(priority=1, plan_id=222, name="Smrdíme", price=2, member_price=2),
        dict(priority=2, plan_id=333, name="Voníme", price=3, member_price=3),
    ]


def test_prepare_tiers_with_extras():
    plans = [
        PlanEntity(
            id="333",
            name="Tarif „Voníme“",
            forSale=True,
            priceCents=300,
            additionalMemberPriceCents=300,
        ),
        PlanEntity(
            id="111",
            name="Tarif „Prdíme“",
            forSale=True,
            priceCents=100,
            additionalMemberPriceCents=0,
        ),
        PlanEntity(
            id="222",
            name="Tarif „Smrdíme“",
            forSale=True,
            priceCents=200,
            additionalMemberPriceCents=200,
        ),
    ]
    extras = {
        "Smrdíme": dict(max_sponsors=4, courses_highlight=True),
        "Prdíme": dict(courses_highlight=True),
    }

    assert prepare_tiers(plans, extras=extras) == [
        dict(
            priority=0,
            plan_id=111,
            name="Prdíme",
            price=1,
            member_price=None,
            courses_highlight=True,
        ),
        dict(
            priority=1,
            plan_id=222,
            name="Smrdíme",
            price=2,
            member_price=2,
            max_sponsors=4,
            courses_highlight=True,
        ),
        dict(
            priority=2,
            plan_id=333,
            name="Voníme",
            price=3,
            member_price=3,
        ),
    ]


def test_prepare_tiers_ignores_individual_plans():
    plans = [
        PlanEntity(
            id="333",
            name="Tarif „Voníme“",
            forSale=True,
            priceCents=300,
            additionalMemberPriceCents=300,
        ),
        PlanEntity(
            id="333",
            name="Angličtina",
            forSale=True,
            priceCents=100,
            additionalMemberPriceCents=None,
        ),
    ]

    assert prepare_tiers(plans) == [
        dict(priority=0, plan_id=333, name="Voníme", price=3, member_price=3),
    ]


def test_prepare_tiers_ignores_private_plans():
    plans = [
        PlanEntity(
            id="333",
            name="Tarif „Voníme“",
            forSale=True,
            priceCents=300,
            additionalMemberPriceCents=300,
        ),
        PlanEntity(
            id="444",
            name="Mentoring „Vrníme“",
            forSale=False,
            priceCents=100,
            additionalMemberPriceCents=0,
        ),
    ]

    assert prepare_tiers(plans) == [
        dict(priority=0, plan_id=333, name="Voníme", price=3, member_price=3),
    ]
