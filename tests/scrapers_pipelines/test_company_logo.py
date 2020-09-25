from pathlib import Path
from io import BytesIO

import pytest
from PIL import Image
from scrapy.pipelines.images import ImageException

from juniorguru.scrapers.pipelines.company_logo import Pipeline


FIXTURES_DIR = Path(__file__).parent / 'fixtures_company_logo'
IMAGES_STORE = str(FIXTURES_DIR)


def _debug(image):
    image.save(FIXTURES_DIR / 'logo-converted.png', 'PNG')


@pytest.fixture
def req():
    class Request():
        url = 'https://example.com/'
    return Request()


@pytest.fixture
def res():
    class Response():
        body = b''
    return Response()


@pytest.fixture
def info():
    class SpiderInfo():
        pass
    return SpiderInfo()


def test_company_logo_image_downloaded_unidentifiable(res, req, info):
    res.body = b'12345'

    with pytest.raises(ImageException, match=r'identified \(https://example\.com/\)'):
        Pipeline(IMAGES_STORE).image_downloaded(res, req, info)


@pytest.mark.parametrize('width, height', [
    (1024, 600),
    (600, 1024),
])
def test_company_logo_image_downloaded_too_large(res, req, info, width, height):
    buffer = BytesIO()
    image = Image.new('RGB', (width, height), (255, 255, 255))
    image.save(buffer, 'PNG')
    buffer.seek(0)
    res.body = buffer.read()

    with pytest.raises(ImageException, match='too large'):
        Pipeline(IMAGES_STORE).image_downloaded(res, req, info)


def test_company_logo_convert_image_has_expected_size():
    logo = Image.open(FIXTURES_DIR / 'logo.png')
    image, buffer = Pipeline(IMAGES_STORE).convert_image(logo)

    assert image.width == Pipeline.SIZE_PX
    assert image.height == Pipeline.SIZE_PX
