from collections import namedtuple

import discord
import pytest

from juniorguru.sync.onboarding.categories import (CHANNELS_PER_CATEGORY_LIMIT,
                                                   ONBOARDING_CATEGORY_NAME,
                                                   has_no_channels,
                                                   is_available_category,
                                                   is_onboarding_category,
                                                   calc_missing_categories_count)


StubChannel = namedtuple('StubChannel', 'name, type')

StubCategory = namedtuple('StubCategory', 'name, type, channels, position',
                          defaults=[ONBOARDING_CATEGORY_NAME, discord.ChannelType.category, [], 0])


def create_channels(count):
    return [StubChannel(f'tipy-{i}', discord.ChannelType.text)
            for i in range(count)]


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
