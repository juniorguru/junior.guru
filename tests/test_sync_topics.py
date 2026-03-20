import pytest
from pydantic import ValidationError

from jg.coop.sync.topics import TopicConfig


def test_topic_config_allows_missing_name_and_icon():
    config = TopicConfig(
        channels=[
            "https://discord.com/channels/769966886598737931/1067439203983568986"
        ],
        pages=["handbook/help.md"],
    )

    assert config.name is None
    assert config.icon is None


def test_topic_config_requires_icon_when_name_is_present():
    with pytest.raises(
        ValidationError,
        match="Topic with a name must also define an icon",
    ):
        TopicConfig(
            name="Otázky a odpovědi",
            channels=[
                "https://discord.com/channels/769966886598737931/1067439203983568986"
            ],
        )
