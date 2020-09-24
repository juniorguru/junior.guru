import tempfile
from pathlib import Path

import pytest
from PIL import Image

from juniorguru.scrapers.pipelines.company_logo import Pipeline


@pytest.fixture
def temp_dir():
    return tempfile.gettempdir()


@pytest.fixture
def logo():
    path = Path(__file__).parent / 'fixtures_company_logo' / 'logo.png'
    return Image.open(path)


# def debug(image):
#     path = Path(__file__).parent / 'fixtures_company_logo' / 'logo-converted.png'
#     image.save(path, 'PNG')


def test_company_logo_convert_image_has_expected_size(temp_dir, logo):
    image, buffer = Pipeline(temp_dir).convert_image(logo)

    assert image.width == Pipeline.SIZE_PX
    assert image.height == Pipeline.SIZE_PX
