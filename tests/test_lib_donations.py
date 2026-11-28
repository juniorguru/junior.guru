import pytest

from jg.coop.lib.brand import BANK_ACCOUNT, BANK_BIC, BANK_IBAN
from jg.coop.lib.donations import coverage_ptc, get_generator, qr_payment_svg


@pytest.mark.parametrize(
    "revenue_breakdown, cost, category, expected",
    [
        ({"donations": 1000, "memberships": 5000}, 10000, "donations", 10),
        ({"donations": 1000, "memberships": 5000}, 10000, "memberships", 50),
        ({"donations": 1999}, 10000, "donations", 19),
        ({"memberships": 5000}, 10000, "donations", 0),
        ({"donations": 20000}, 10000, "donations", 200),
    ],
)
def test_coverage_ptc(
    revenue_breakdown: dict[str, int], cost: int, category: str, expected: int
):
    assert coverage_ptc(revenue_breakdown, cost, category) == expected


@pytest.mark.parametrize("cost", [0, -100])
def test_coverage_ptc_no_cost(cost: int):
    assert coverage_ptc({"donations": 1000}, cost, "donations") is None


def test_get_generator():
    generator = get_generator(
        "2501717332/2010", "FIOBCZPPXXX", 499, "444222", "LOVE pro junior.guru"
    )

    assert generator.get_text() == (
        "SPD*1.0*ACC:CZ8420100000002501717332+FIOBCZPPXXX*AM:499.00*CC:CZK"
        "*MSG:LOVE pro junior.guru*X-VS:444222"
    )


def test_brand_iban_matches_account():
    generator = get_generator(BANK_ACCOUNT, BANK_BIC, 499, "444222", "LOVE")

    assert f"ACC:{BANK_IBAN.replace(' ', '')}+{BANK_BIC}*" in generator.get_text()


def test_qr_payment_svg_is_inline_svg():
    svg = qr_payment_svg("2501717332/2010", "FIOBCZPPXXX", 499, "444222", "LOVE")

    assert svg.startswith("<svg ")


def test_qr_payment_svg_encodes_payment():
    svg_499 = qr_payment_svg("2501717332/2010", "FIOBCZPPXXX", 499, "444222", "LOVE")
    svg_500 = qr_payment_svg("2501717332/2010", "FIOBCZPPXXX", 500, "444222", "LOVE")

    assert svg_499 != svg_500
