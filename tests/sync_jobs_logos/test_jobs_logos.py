from pathlib import Path

import pytest
from PIL import Image

from jg.coop.models.job import LogoSourceType
from jg.coop.sync.jobs_logos import (
    SIZE_PX,
    Logo,
    convert_image,
    get_logo_basename,
    get_unused_paths,
    sort_key,
)


FIXTURES_DIR = Path(__file__).parent


def _debug(image):
    image.save(FIXTURES_DIR / "logo-converted.webp", "WEBP")


@pytest.fixture
def logo_image_data() -> dict:
    return {
        "image_url": "https://apify.example.com/kvs/image.webp",
        "original_image_url": "https://example.com/image.webp",
        "width": SIZE_PX,
        "height": SIZE_PX,
        "format": "webp",
        "source_url": "https://example.com",
    }


def test_company_logo_convert_image_has_expected_size():
    logo = Image.open(FIXTURES_DIR / "logo.png")
    image = convert_image(logo)

    assert image.width == SIZE_PX
    assert image.height == SIZE_PX


def test_sort_key_prefers_logo_over_icon(logo_image_data: dict):
    key1 = sort_key(
        Logo(image=logo_image_data, source_type=LogoSourceType.ICON),
    )
    key2 = sort_key(
        Logo(image=logo_image_data, source_type=LogoSourceType.LOGO),
    )

    assert key2 < key1


def test_sort_key_treats_small_images_like_squares(logo_image_data: dict):
    key1 = sort_key(
        Logo(
            image=logo_image_data | {"width": 1, "height": 16},
            source_type=LogoSourceType.ICON,
        )
    )
    key2 = sort_key(
        Logo(
            image=logo_image_data | {"width": 4, "height": 4},
            source_type=LogoSourceType.ICON,
        )
    )

    assert key1 == key2


def test_sort_key_prefers_squares(logo_image_data: dict):
    key1 = sort_key(
        Logo(
            image=logo_image_data | {"width": 100, "height": 1600},
            source_type=LogoSourceType.LOGO,
        )
    )
    key2 = sort_key(
        Logo(
            image=logo_image_data | {"width": 400, "height": 400},
            source_type=LogoSourceType.LOGO,
        )
    )

    assert key2 < key1


def test_sort_key_prefers_square_like_rectangles(logo_image_data: dict):
    key1 = sort_key(
        Logo(
            image=logo_image_data | {"width": 100, "height": 1600},
            source_type=LogoSourceType.LOGO,
        )
    )
    key2 = sort_key(
        Logo(
            image=logo_image_data | {"width": 305, "height": 300},
            source_type=LogoSourceType.LOGO,
        )
    )

    assert key2 < key1


def test_sort_key_prefers_larger_images(logo_image_data: dict):
    key1 = sort_key(
        Logo(
            image=logo_image_data | {"width": 500, "height": 500},
            source_type=LogoSourceType.LOGO,
        )
    )
    key2 = sort_key(
        Logo(
            image=logo_image_data | {"width": 1000, "height": 1000},
            source_type=LogoSourceType.LOGO,
        )
    )

    assert key2 < key1


@pytest.mark.parametrize(
    "image_url, expected",
    [
        (
            "https://api.apify.com/v2/key-value-stores/abc123/records/f00d?signature=xyz",
            "f00d",
        ),
        ("https://api.apify.com/v2/key-value-stores/def456/records/f00d", "f00d"),
        ("https://api.apify.com/v2/key-value-stores/abc123/records/f00d/", "f00d"),
    ],
)
def test_get_logo_basename(image_url: str, expected: str):
    assert get_logo_basename(image_url) == expected


def test_get_unused_paths():
    paths = [Path("a.webp"), Path("b.webp"), Path("unknown.webp")]
    used_paths = [Path("b.webp")]

    assert get_unused_paths(paths, used_paths, keep={"unknown.webp"}) == [
        Path("a.webp")
    ]
