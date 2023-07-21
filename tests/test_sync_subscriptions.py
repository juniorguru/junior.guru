import pytest

from juniorguru.sync.subscriptions import (activities_from_subscription,
                                           classify_marketing_survey_answer,
                                           classify_referrer)


def test_activities_from_subscription():
    assert activities_from_subscription  # TODO


@pytest.mark.parametrize('url, expected', [
    ('https://junior.guru/', '/'),
    ('https://junior.guru/learn/', '/learn'),
    ('https://junior.guru/events/?fbclid=IwAR0WkuqPqg7z6GHW-vEGgWlhgpzcT62qJkarSOrOQTsUjzxRBbSS8RGMw8I', '/events'),
    ('https://t.co', 'twitter'),
    ('https://t.co/RExQZc2z4V?amp=1', 'twitter'),
    ('https://www.linkedin.com/', 'linkedin'),
    ('https://l.facebook.com/', 'facebook'),
    ('http://m.facebook.com', 'facebook'),
    ('android-app://m.facebook.com/', 'facebook'),
    ('https://honzajavorek.cz/', 'honzajavorek'),
    ('https://honzajavorek.cz/blog/tydenni-poznamky-37-prvni-klubovy-sraz/', 'weeknotes'),
    ('https://www.youtube.com/', 'youtube'),
    ('https://www.google.com', 'google'),
    ('https://www.patreon.com/', 'other'),
])
def test_classify_referrer(url, expected):
    assert classify_referrer(url) == expected


@pytest.mark.parametrize('text, expected', [
    ('Google', 'search'),
    ('Youtube', 'youtube'),
    ('Youtube videá od "Yablko"', 'yablko'),
    ('Cez video od yablka.', 'yablko'),
    ('bla bla', 'other'),
])
def test_classify_marketing_survey_answer(text, expected):
    assert classify_marketing_survey_answer(text) == expected


# def test_get_subscribed_periods():
#     subscription = {'id': '123456789',
#                     'active': True,
#                     'createdAt': 1629300930,
#                     'expiresAt': 1654097730,
#                     'trialStartAt': 1629300930,
#                     'trialEndAt': 1630510530,
#                     'coupon': None,
#                     'member': {},
#                     'orders': [
#                         {'createdAt': 1651419692, 'coupon': None},
#                         {'createdAt': 1648827722, 'coupon': None},
#                         {'createdAt': 1646149282, 'coupon': None},
#                         {'createdAt': 1643730158, 'coupon': None},
#                         {'createdAt': 1641051710, 'coupon': None},
#                         {'createdAt': 1638373347, 'coupon': None},
#                         {'createdAt': 1635781082, 'coupon': {'code': 'COUPON12345678'}},
#                         {'createdAt': 1633103366, 'coupon': {'code': 'STUDENTGARGAMEL69320144V2'}},
#                         {'createdAt': 1630510548, 'coupon': {'code': 'COUPON12345678'}},
#                         {'createdAt': 1629300930, 'coupon': None}
#                     ]}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2022, 5, 1), 'end_on': date(2022, 5, 31), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2022, 4, 1), 'end_on': date(2022, 4, 30), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2022, 3, 1), 'end_on': date(2022, 3, 31), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2022, 2, 1), 'end_on': date(2022, 2, 28), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2022, 1, 1), 'end_on': date(2022, 1, 31), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2021, 12, 1), 'end_on': date(2021, 12, 31), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2021, 11, 1), 'end_on': date(2021, 11, 30), 'coupon': 'COUPON12345678', 'is_trial': False},
#         {'start_on': date(2021, 10, 1), 'end_on': date(2021, 10, 31), 'coupon': 'STUDENTGARGAMEL69320144V2', 'is_trial': False},
#         {'start_on': date(2021, 9, 1), 'end_on': date(2021, 9, 30), 'coupon': 'COUPON12345678', 'is_trial': False},
#         {'start_on': date(2021, 8, 18), 'end_on': date(2021, 8, 31), 'coupon': None, 'is_trial': True},
#     ]


# def test_get_subscribed_periods_different_created_at():
#     subscription = {'id': '123456789',
#                     'active': True,
#                     'createdAt': 1619817670,
#                     'expiresAt': 1652563270,
#                     'coupon': None,
#                     'member': {},
#                     'orders': [
#                         {'coupon': None, 'createdAt': 1621027502},
#                         {'coupon': None, 'createdAt': 1619817671}
#                     ]}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2021, 5, 14), 'end_on': date(2022, 5, 13), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2021, 4, 30), 'end_on': date(2021, 5, 13), 'coupon': None, 'is_trial': False},
#     ]


# def test_get_subscribed_periods_no_orders():
#     subscription = {'id': '123456789',
#                     'active': True,
#                     'createdAt': 1619817670,
#                     'expiresAt': 1652563270,
#                     'coupon': None,
#                     'member': {},
#                     'orders': []}

#     assert list(get_subscribed_periods(subscription)) == []


# def test_get_subscribed_periods_coupon():
#     subscription = {'active': True,
#                     'coupon': None,
#                     'createdAt': 1660041421,
#                     'expiresAt': 1692787021,
#                     'id': '123456789',
#                     'member': {},
#                     'orders': [{'coupon': {'code': 'TEAM666'}, 'createdAt': 1661251317},
#                                {'coupon': None, 'createdAt': 1660041421}],
#                     'plan': {'intervalUnit': 'year'},
#                     'trialEndAt': 1661251021,
#                     'trialStartAt': 1660041421}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2022, 8, 23), 'end_on': date(2023, 8, 22), 'coupon': 'TEAM666', 'is_trial': False},
#         {'start_on': date(2022, 8, 9), 'end_on': date(2022, 8, 22), 'coupon': None, 'is_trial': True},
#     ]


# def test_get_subscribed_periods_subscription_coupon_overlaps_order_coupon():
#     subscription = {'active': True,
#                     'coupon': {'code': 'TEAM666'},
#                     'createdAt': 1636922909,
#                     'expiresAt': 1704897133,
#                     'id': '123456789',
#                     'member': {},
#                     'orders': [{'coupon': {'code': 'COMPANY123'},
#                                 'createdAt': 1669668703},
#                                {'coupon': {'code': 'COMPANY123'},
#                                  'createdAt': 1638132692},
#                                {'coupon': None, 'createdAt': 1636922909}],
#                     'plan': {'intervalUnit': 'year'},
#                     'trialEndAt': 1638132509,
#                     'trialStartAt': 1636922909}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2022, 11, 28), 'end_on': date(2024, 1, 9), 'coupon': 'TEAM666', 'is_trial': False},
#         {'start_on': date(2021, 11, 28), 'end_on': date(2022, 11, 27), 'coupon': 'COMPANY123', 'is_trial': False},
#         {'start_on': date(2021, 11, 14), 'end_on': date(2021, 11, 27), 'coupon': None, 'is_trial': True},
#     ]


# def test_get_subscribed_periods_subscription_coupon_overlaps_trial():
#     subscription = {'active': True,
#                     'coupon': {'code': 'TEAM666'},
#                     'createdAt': 1673613241,
#                     'expiresAt': 1674822841,
#                     'id': '123456789',
#                     'member': {},
#                     'orders': [{'coupon': None, 'createdAt': 1673613241}],
#                     'plan': {'intervalUnit': 'year'},
#                     'trialEndAt': 1674822841,
#                     'trialStartAt': 1673613241}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2023, 1, 13), 'end_on': date(2023, 1, 26), 'coupon': 'TEAM666', 'is_trial': True},
#     ]


# def test_get_subscribed_periods_with_gap():
#     subscription = {'id': '123456789',
#                     'active': True,
#                     'createdAt': 1677080166,
#                     'expiresAt': 1689578220,
#                     'trialStartAt': 1677080166,
#                     'trialEndAt': 1678289766,
#                     'coupon': None,
#                     'orders': [{'createdAt': 1684307820, 'coupon': None},
#                                {'createdAt': 1678327037, 'coupon': None},
#                                {'createdAt': 1677080166, 'coupon': None},
#                                {'createdAt': 1686986457, 'coupon': None}],
#                     'plan': {'intervalUnit': 'month'}}

#     assert list(get_subscribed_periods(subscription)) == [
#         {'start_on': date(2023, 6, 17), 'end_on': date(2023, 7, 16), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2023, 5, 17), 'end_on': date(2023, 6, 16), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2023, 3, 9), 'end_on': date(2023, 4, 8), 'coupon': None, 'is_trial': False},
#         {'start_on': date(2023, 2, 22), 'end_on': date(2023, 3, 8), 'coupon': None, 'is_trial': True},
#     ]
