from pathlib import Path

from PIL import Image

from juniorguru.sync.jobs_logos import SIZE_PX, convert_image, sort_key, unique


FIXTURES_DIR = Path(__file__).parent


def _debug(image):
    image.save(FIXTURES_DIR / 'logo-converted.png', 'PNG')


def test_company_logo_convert_image_has_expected_size():
    logo = Image.open(FIXTURES_DIR / 'logo.png')
    image = convert_image(logo)

    assert image.width == SIZE_PX
    assert image.height == SIZE_PX


def test_sort_key_prefers_successfully_downloaded_images():
    key1 = sort_key(dict(image_path=None,
                         type='logo',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))

    assert key2 < key1


def test_sort_key_prefers_successfully_downloaded_images_even_if_icon():
    key1 = sort_key(dict(image_path=None,
                         type='logo',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='icon',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))

    assert key2 < key1


def test_sort_key_prefers_logo_over_icon():
    key1 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='icon',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=SIZE_PX,
                         orig_height=SIZE_PX))

    assert key2 < key1


def test_sort_key_treats_small_images_like_squares():
    key1 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='icon',
                         orig_width=1,
                         orig_height=16))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='icon',
                         orig_width=4,
                         orig_height=4))

    assert key1 == key2


def test_sort_key_prefers_squares():
    key1 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=100,
                         orig_height=1600))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=400,
                         orig_height=400))

    assert key2 < key1


def test_sort_key_prefers_square_like_rectangles():
    key1 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=100,
                         orig_height=1600))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=305,
                         orig_height=300))

    assert key2 < key1


def test_sort_key_prefers_larger_images():
    key1 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=500,
                         orig_height=500))
    key2 = sort_key(dict(image_path='path/to/somewhere.png',
                         type='logo',
                         orig_width=1000,
                         orig_height=1000))

    assert key2 < key1


def test_unique():
    assert sorted(unique([1, 3, 5, 3, 6, 0, 1])) == sorted([1, 3, 5, 6, 0])


def test_unique_returns_list():
    assert isinstance(unique([1, 3, 5, 3]), list)


def test_unique_skips_none():
    assert sorted(unique([1, 3, None, 5, 3, None, 6, 0, 1])) == sorted([1, 3, 5, 6, 0])
