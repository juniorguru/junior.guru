import json
from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from jg.coop.models.podcast import (
    PODCAST_NAME,
    PodcastEpisode,
    podcast_series_json_ld,
)


def test_publish_at_prg():
    podcast_episode = PodcastEpisode(publish_on=date(2023, 2, 10))
    expected = datetime(
        2023, 2, 10, 1, 42, 42, tzinfo=ZoneInfo("Europe/Prague")
    ).utctimetuple()

    assert podcast_episode.publish_at_prg.utctimetuple() == expected


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, "Adéla (Company) about testing"),
        ({"number": True, "affiliation": True}, "#1 Adéla (Company) about testing"),
        ({"number": False, "affiliation": True}, "Adéla (Company) about testing"),
        ({"number": True, "affiliation": False}, "#1 Adéla about testing"),
        ({"number": False, "affiliation": False}, "Adéla about testing"),
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
        ({}, "Adéla about testing"),
        ({"number": True, "affiliation": True}, "#1 Adéla about testing"),
        ({"number": False, "affiliation": True}, "Adéla about testing"),
        ({"number": True, "affiliation": False}, "#1 Adéla about testing"),
        ({"number": False, "affiliation": False}, "Adéla about testing"),
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
        ({}, "About testing"),
        ({"number": True, "affiliation": True}, "#1 About testing"),
        ({"number": False, "affiliation": True}, "About testing"),
        ({"number": True, "affiliation": False}, "#1 About testing"),
        ({"number": False, "affiliation": False}, "About testing"),
    ],
)
def test_format_title_with_no_guest(kwargs, expected):
    podcast_episode = PodcastEpisode(number=1, title="About testing")

    assert podcast_episode.format_title(**kwargs) == expected


def test_to_json_ld():
    podcast_episode = PodcastEpisode(
        number=42,
        publish_on=date(2023, 2, 10),
        title="about testing",
        guest_name="Adéla",
        guest_affiliation="Company",
        image_path="podcast/42.jpg",
        media_url="https://example.com/42.mp3",
        media_size=1000,
        media_type="audio/mpeg",
        media_duration_s=3600,
        description="Description",
    )

    assert json.loads(podcast_episode.to_json_ld()) == {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "associatedMedia": {
            "@type": "MediaObject",
            "contentSize": "1000",
            "contentUrl": "https://example.com/42.mp3",
            "encodingFormat": "audio/mpeg",
        },
        "datePublished": "2023-02-10",
        "description": "Description",
        "duration": "PT3600S",
        "episodeNumber": 42,
        "image": "https://junior.guru/static/podcast/42.jpg",
        "inLanguage": "cs",
        "name": "Adéla (Company) about testing",
        "partOfSeries": {
            "@type": "PodcastSeries",
            "@id": "https://junior.guru/podcast/#series",
            "name": PODCAST_NAME,
            "url": "https://junior.guru/podcast/",
        },
        "url": "https://junior.guru/podcast/42/",
    }


def test_podcast_series_json_ld():
    data = json.loads(podcast_series_json_ld())

    assert data["@id"] == "https://junior.guru/podcast/#series"


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {"guest_name": "Jiří Psotka", "guest_affiliation": "Red Hat"},
            "V 1. dílu Junior Guru podcastu je hostem Jiří Psotka (Red Hat).",
        ),
        (
            {"guest_name": "Adéla", "guest_has_feminine_name": True},
            "V 1. dílu Junior Guru podcastu je hostkou Adéla.",
        ),
        (
            {"guest_name": "Karolina Surma a Petr Viktorin"},
            "V 1. dílu Junior Guru podcastu jsou hosty Karolina Surma a Petr Viktorin.",
        ),
        ({}, "V 1. dílu Junior Guru podcastu: Startujeme!"),
    ],
)
def test_page_description(kwargs: dict, expected: str):
    podcast_episode = PodcastEpisode(number=1, title="Startujeme!", **kwargs)

    assert podcast_episode.page_description == expected
