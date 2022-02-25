from pathlib import Path
from io import BytesIO

import pytest
from PIL import Image
from scrapy.pipelines.images import ImageException, ImagesPipeline

from juniorguru.jobs.legacy_jobs.pipelines.company_logo import Pipeline, load_orig_size, select_company_logo


FIXTURES_DIR = Path(__file__).parent / 'fixtures_company_logo'


def _debug(image):
    image.save(FIXTURES_DIR / 'logo-converted.png', 'PNG')


@pytest.fixture
def pipeline():
    item_completed = ImagesPipeline.item_completed
    ImagesPipeline.item_completed = lambda self, results, item, info: item
    yield Pipeline(str(FIXTURES_DIR))
    ImagesPipeline.item_completed = item_completed


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


def test_load_orig_size():
    assert load_orig_size(FIXTURES_DIR / 'logo-orig140x75.png') == (140, 75)


def test_select_company_logo_selects_the_first_by_default():
    company_logos = [dict(path='1.png'),
                     dict(path='2.png')]
    orig_sizes = [(300, 300),
                  (300, 300)]

    assert select_company_logo(company_logos, orig_sizes, 100) == dict(path='1.png')


def test_select_company_logo_selects_larger():
    company_logos = [dict(path='1.png'),
                     dict(path='2.png')]
    orig_sizes = [(300, 300),
                  (500, 500)]

    assert select_company_logo(company_logos, orig_sizes, 100) == dict(path='2.png')


def test_select_company_logo_selects_square_even_if_smaller():
    company_logos = [dict(path='1.png'),
                     dict(path='2.png')]
    orig_sizes = [(300, 300),
                  (400, 500)]

    assert select_company_logo(company_logos, orig_sizes, 100) == dict(path='1.png')


def test_select_company_logo_selects_larger_non_square_if_images_are_small():
    company_logos = [dict(path='1.png'),
                     dict(path='2.png')]
    orig_sizes = [(30, 30),
                  (40, 50)]

    assert select_company_logo(company_logos, orig_sizes, 100) == dict(path='2.png')


def test_item_completed_sets_company_logo(pipeline, item, info):
    item['company_logos'] = [
        {
            'checksum': '6b874bd7b996e9323fd2e094be83ca4c',
            'path': 'logo-orig16x16.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/d6e95f8c946b72f36783aa0a0238341b.png'
        },
        {
            'checksum': 'f3e2f82d7d8b24367f0a2c24b3d1aea3',
            'path': 'logo-orig180x180.png',
            'status': 'uptodate',
            'url': 'https://www.startupjobs.cz/uploads/GQ1A8RDZWYUJfavicon155377551420.png'
        },
    ]
    item = pipeline.item_completed([], item, info)

    assert item['company_logo_path'] == 'images/logo-orig180x180.png'
