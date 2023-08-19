from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from juniorguru.models.podcast import PodcastEpisode


def test_publish_at_prg():
    podcast_episode = PodcastEpisode(publish_on=date(2023, 2, 10))
    expected = datetime(
        2023, 2, 10, 1, 42, 42, tzinfo=ZoneInfo("Europe/Prague")
    ).utctimetuple()

    assert podcast_episode.publish_at_prg.utctimetuple() == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (dict(), "Adéla (Company) about testing"),
        (dict(number=True, affiliation=True), "#1 Adéla (Company) about testing"),
        (dict(number=False, affiliation=True), "Adéla (Company) about testing"),
        (dict(number=True, affiliation=False), "#1 Adéla about testing"),
        (dict(number=False, affiliation=False), "Adéla about testing"),
    ],
)
def test_format_title(kwargs, expected):
    podcast_episode = PodcastEpisode(
        number=1, guest_name="Adéla", guest_affiliation="Company", title="about testing"
    )

    assert podcast_episode.format_title(**kwargs) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (dict(), "Adéla about testing"),
        (dict(number=True, affiliation=True), "#1 Adéla about testing"),
        (dict(number=False, affiliation=True), "Adéla about testing"),
        (dict(number=True, affiliation=False), "#1 Adéla about testing"),
        (dict(number=False, affiliation=False), "Adéla about testing"),
    ],
)
def test_format_title_with_no_affiliation(kwargs, expected):
    podcast_episode = PodcastEpisode(
        number=1, guest_name="Adéla", title="about testing"
    )

    assert podcast_episode.format_title(**kwargs) == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (dict(), "About testing"),
        (dict(number=True, affiliation=True), "#1 About testing"),
        (dict(number=False, affiliation=True), "About testing"),
        (dict(number=True, affiliation=False), "#1 About testing"),
        (dict(number=False, affiliation=False), "About testing"),
    ],
)
def test_format_title_with_no_guest(kwargs, expected):
    podcast_episode = PodcastEpisode(number=1, title="About testing")

    assert podcast_episode.format_title(**kwargs) == expected
