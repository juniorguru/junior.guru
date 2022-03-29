from pathlib import Path

from PIL import Image

from juniorguru.sync.jobs_logos import convert_image, SIZE_PX


FIXTURES_DIR = Path(__file__).parent


def _debug(image):
    image.save(FIXTURES_DIR / 'logo-converted.png', 'PNG')


def test_company_logo_convert_image_has_expected_size():
    logo = Image.open(FIXTURES_DIR / 'logo.png')
    image = convert_image(logo)

    assert image.width == SIZE_PX
    assert image.height == SIZE_PX
