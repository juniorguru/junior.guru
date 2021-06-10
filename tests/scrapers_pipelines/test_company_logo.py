from pathlib import Path
from io import BytesIO

import pytest
from PIL import Image
from scrapy.pipelines.images import ImageException

from juniorguru.scrapers.pipelines.company_logo import Pipeline


FIXTURES_DIR = Path(__file__).parent / 'fixtures_company_logo'


def _debug(image):
    image.save(FIXTURES_DIR / 'logo-converted.png', 'PNG')


@pytest.fixture
def pipeline():
    return Pipeline(str(FIXTURES_DIR))


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


def test_company_logo_image_downloaded_unidentifiable(pipeline, res, req, info):
    res.body = b'12345'

    with pytest.raises(ImageException, match=r'identified \(https://example\.com/\)'):
        pipeline.image_downloaded(res, req, info)


@pytest.mark.parametrize('width, height', [
    (1024, 600),
    (600, 1024),
])
def test_company_logo_image_downloaded_too_large(pipeline, res, req, info, width, height):
    buffer = BytesIO()
    image = Image.new('RGB', (width, height), (255, 255, 255))
    image.save(buffer, 'PNG')
    buffer.seek(0)
    res.body = buffer.read()

    with pytest.raises(ImageException, match='too large'):
        pipeline.image_downloaded(res, req, info)


def test_company_logo_convert_image_has_expected_size(pipeline):
    logo = Image.open(FIXTURES_DIR / 'logo.png')
    image, buffer = pipeline.convert_image(logo)

    assert image.width == Pipeline.size_px
    assert image.height == Pipeline.size_px


def test_get_company_logo_path_chooses_first_if_all_same_size(pipeline, item, info):
    pipeline.orig_sizes.update({
        'company-logos/d40730d4068db31a09687ebb42f7637e26864a30.png': (40, 40),
        'company-logos/d1eed8447fb59dc9587dd97148a109a3cca77ed8.png': (40, 40),
    })
    item['company_logos'] = [
        {
            'checksum': '6b874bd7b996e9323fd2e094be83ca4c',
            'path': 'company-logos/d40730d4068db31a09687ebb42f7637e26864a30.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/d6e95f8c946b72f36783aa0a0238341b.png'
        },
        {
            'checksum': 'f3e2f82d7d8b24367f0a2c24b3d1aea3',
            'path': 'company-logos/d1eed8447fb59dc9587dd97148a109a3cca77ed8.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/GQ1A8RDZWYUJfavicon155377551420.png'
        },
    ]
    item = pipeline.item_completed([], item, info)

    assert item['company_logo_path'] == 'images/company-logos/d40730d4068db31a09687ebb42f7637e26864a30.png'
