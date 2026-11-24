from datetime import date

import pytest
from pydantic import ValidationError

from jg.coop.sync.events import EventConfig


def make_event_config(**kwargs) -> EventConfig:
    return EventConfig(
        id=1,
        title=kwargs.get("title", "Short title"),
        date=date(2026, 11, 25),
        description="Description",
        bio_name=kwargs.get("bio_name", "Ada Lovelace"),
        bio="Bio",
    )


def test_event_config_full_title_fits_discord():
    event_config = make_event_config(title="x" * 86)

    assert event_config.title == "x" * 86


def test_event_config_full_title_too_long_for_discord():
    with pytest.raises(ValidationError, match="101 characters"):
        make_event_config(title="x" * 87)
