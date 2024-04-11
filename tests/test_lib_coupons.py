import pytest

from jg.coop.lib import coupons


@pytest.mark.parametrize(
    "coupon, expected",
    [
        ("GARGAMEL", dict(slug="gargamel", coupon="GARGAMEL")),
        (
            "FAKTUROID123456",
            dict(slug="fakturoid", suffix="123456", coupon="FAKTUROID123456"),
        ),
        (
            "CDN77COM123456",
            dict(slug="cdn77com", suffix="123456", coupon="CDN77COM123456"),
        ),
        (
            "STUDENTGARGAMEL69320144",
            dict(
                slug="studentgargamel",
                suffix="69320144",
                coupon="STUDENTGARGAMEL69320144",
            ),
        ),
    ],
)
def test_parse_coupon(coupon, expected):
    assert coupons.parse_coupon(coupon) == expected


def test_parse_coupon_raises_on_wrong_input():
    with pytest.raises(TypeError):
        coupons.parse_coupon(None)
