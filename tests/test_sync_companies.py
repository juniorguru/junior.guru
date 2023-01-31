from juniorguru.sync.companies import get_coupons_mapping


def test_get_coupons_mapping():
    assert get_coupons_mapping([
        {'code': 'FOO123123123', 'state': 'enabled'},
        {'code': 'BOO456456456', 'state': 'enabled'},
        {'code': 'STUDENTBOO456456456', 'state': 'enabled'},
        {'code': 'MOO666666666', 'state': 'disabled'},
    ]) == {
        'foo': {'coupon': 'FOO123123123'},
        'boo': {'coupon': 'BOO456456456', 'student_coupon': 'STUDENTBOO456456456'},
    }
