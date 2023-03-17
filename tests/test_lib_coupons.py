import pytest

from juniorguru.lib import coupons


@pytest.mark.parametrize('coupon, expected', [
    ('GARGAMEL', dict(name='GARGAMEL',
                      coupon='GARGAMEL',
                      is_student=False)),
    ('FAKTUROID123456', dict(name='FAKTUROID',
                             suffix='123456',
                             coupon='FAKTUROID123456',
                             is_student=False)),
    ('CDN77COM123456', dict(name='CDN77COM',
                            suffix='123456',
                            coupon='CDN77COM123456',
                            is_student=False)),
    ('STUDENTGARGAMEL69320144', dict(name='STUDENTGARGAMEL',
                                     suffix='69320144',
                                     coupon='STUDENTGARGAMEL69320144',
                                     is_student=True)),
])
def test_parse_coupon(coupon, expected):
    assert coupons.parse_coupon(coupon) == expected


def test_parse_coupon_raises_on_wrong_input():
    with pytest.raises(TypeError):
        coupons.parse_coupon(None)
