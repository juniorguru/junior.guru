from datetime import date
from pathlib import Path

import pytest
import yaml

from jg.coop.sync.podcast import PodcastEpisodeConfig, parse_episode


def create_config(**kwargs) -> PodcastEpisodeConfig:
    return PodcastEpisodeConfig(
        **{
            "number": 7,
            "title": "o testování",
            "guest_name": "Adéla Nováková",
            "guest_has_feminine_name": True,
            "guest_affiliation": "Company",
            "publish_on": date(2022, 7, 17),
            "description": "Popis",
            "image_path": "avatars-participants/adela.jpg",
            "media_size": 21636733,
            "media_duration_s": 1545,
            **kwargs,
        }
    )


def test_parse_episode_media_url():
    record = parse_episode(create_config())

    assert record["media_url"] == "https://podcast.junior.guru/episodes/0007.mp3"


def test_parse_episode_media_slug():
    record = parse_episode(create_config())

    assert record["media_slug"] == "0007"


def test_parse_episode_media_type():
    record = parse_episode(create_config())

    assert record["media_type"] == "audio/mpeg"


@pytest.mark.parametrize("guest_has_feminine_name", [True, False])
def test_parse_episode_guest_has_feminine_name(guest_has_feminine_name: bool):
    config = create_config(guest_has_feminine_name=guest_has_feminine_name)
    record = parse_episode(config)

    assert record["guest_has_feminine_name"] is guest_has_feminine_name


def test_parse_episode_without_guest():
    config = create_config(
        guest_name=None, guest_has_feminine_name=None, guest_affiliation=None
    )
    record = parse_episode(config)

    assert record["guest_has_feminine_name"] is None


def test_parse_episode_guest_missing_feminine_name_flag():
    config = create_config(guest_has_feminine_name=None)

    with pytest.raises(ValueError, match="guest_has_feminine_name"):
        parse_episode(config)


@pytest.mark.parametrize(
    "guest_has_feminine_name, guest_affiliation",
    [
        (None, "Company"),
        (True, None),
    ],
)
def test_parse_episode_missing_guest_name(
    guest_has_feminine_name: bool | None, guest_affiliation: str | None
):
    config = create_config(
        guest_name=None,
        guest_has_feminine_name=guest_has_feminine_name,
        guest_affiliation=guest_affiliation,
    )

    with pytest.raises(ValueError, match="guest_name"):
        parse_episode(config)


def test_podcast_yaml_is_valid():
    path = Path(__file__).parent.parent / "src/jg/coop/data/podcast.yml"
    yaml_data = yaml.safe_load(path.read_text())

    assert all(parse_episode(PodcastEpisodeConfig(**record)) for record in yaml_data)
