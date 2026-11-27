import pytest

from jg.coop.lib.donations import coverage_ptc, qr_payment_spayd, qr_payment_svg


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


def test_qr_payment_spayd():
    assert qr_payment_spayd(
        "2501717332/2010", "FIOBCZPPXXX", 499, "444222", "LOVE pro junior.guru"
    ) == (
        "SPD*1.0*ACC:CZ8420100000002501717332+FIOBCZPPXXX*AM:499.00*CC:CZK"
        "*MSG:LOVE pro junior.guru*X-VS:444222"
    )


def test_qr_payment_svg_is_inline_svg():
    svg = qr_payment_svg("2501717332/2010", "FIOBCZPPXXX", 499, "444222", "LOVE")

    assert svg.startswith("<svg ")
