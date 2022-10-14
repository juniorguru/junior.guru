from collections import namedtuple

import discord
import pytest

from juniorguru.sync.onboarding.categories import (CHANNELS_PER_CATEGORY_LIMIT,
                                                   ONBOARDING_CATEGORY_NAME,
                                                   NoOnboardingCategoriesAvailableError,
                                                   calc_missing_categories_count,
                                                   get_available_category,
                                                   has_no_channels,
                                                   is_available_category,
                                                   is_onboarding_category)


StubChannel = namedtuple('StubChannel', 'name, type',
                         defaults=['sample-channel-name', discord.ChannelType.text])

StubCategory = namedtuple('StubCategory', 'name, type, channels, position',
                          defaults=[ONBOARDING_CATEGORY_NAME, discord.ChannelType.category, [], 0])


def create_channels(count):
    return [StubChannel(f'tipy-{i}') for i in range(count)]


def test_create_channels_helps_creating_given_number_of_channels():
    assert len(create_channels(42)) == 42


@pytest.mark.parametrize('name, type, expected', [
    ('foo', discord.ChannelType.text, False),
    (ONBOARDING_CATEGORY_NAME, discord.ChannelType.text, False),
    ('foo', discord.ChannelType.category, False),
    (ONBOARDING_CATEGORY_NAME, discord.ChannelType.category, True),
])
def test_is_onboarding_category(name, type, expected):
    channel = StubChannel(name, type)

    assert is_onboarding_category(channel) is expected


@pytest.mark.parametrize('channels_count, expected', [
    (10000, False),
    (CHANNELS_PER_CATEGORY_LIMIT + 1, False),
    (CHANNELS_PER_CATEGORY_LIMIT, False),
    (CHANNELS_PER_CATEGORY_LIMIT - 1, True),
    (1, True),
    (0, True),
])
def test_is_available_category(channels_count, expected):
    category = StubCategory(channels=create_channels(channels_count))

    assert is_available_category(category) is expected


@pytest.mark.parametrize('channels_count, expected', [
    (10000, False),
    (CHANNELS_PER_CATEGORY_LIMIT + 1, False),
    (CHANNELS_PER_CATEGORY_LIMIT, False),
    (CHANNELS_PER_CATEGORY_LIMIT - 1, False),
    (1, False),
    (0, True),
])
def test_has_no_channels(channels_count, expected):
    category = StubCategory(channels=create_channels(channels_count))

    assert has_no_channels(category) is expected


@pytest.mark.parametrize('existing_categories_count, max_channels_needed, expected', [
    (0, 0, 0),
    (0, 10, 1),
    (0, 42, 1),
    (1, 42, 0),
    (1, 55, 1),
    (2, 55, 0),
    (1, 233, 4),
    (3, 300, 3),
])
def test_calc_missing_categories_count(existing_categories_count, max_channels_needed, expected):
    assert calc_missing_categories_count(existing_categories_count, max_channels_needed) == expected


def test_get_available_category():
    categories = [StubCategory(channels=create_channels(CHANNELS_PER_CATEGORY_LIMIT)),
                  StubCategory(channels=create_channels(CHANNELS_PER_CATEGORY_LIMIT)),
                  StubCategory(channels=create_channels(2))]

    assert get_available_category(categories) == categories[2]


def test_get_available_category_raises_no_categories():
    categories = []

    with pytest.raises(NoOnboardingCategoriesAvailableError):
        get_available_category(categories)


def test_get_available_category_skips_channels_and_non_onboarding_categories():
    categories = [StubChannel(),
                  StubChannel(),
                  StubCategory(channels=[], name='foo'),
                  StubCategory(channels=create_channels(5))]

    assert get_available_category(categories) == categories[3]


def test_get_available_category_raises_no_available_categories():
    categories = [StubCategory(channels=create_channels(CHANNELS_PER_CATEGORY_LIMIT)),
                  StubCategory(channels=create_channels(CHANNELS_PER_CATEGORY_LIMIT))]

    with pytest.raises(NoOnboardingCategoriesAvailableError):
        get_available_category(categories)


def test_get_available_category_sorts_by_position():
    categories = [StubCategory(channels=create_channels(1), position=50),
                  StubCategory(channels=create_channels(5), position=10),
                  StubCategory(channels=create_channels(2), position=30)]

    assert get_available_category(categories) == categories[1]
