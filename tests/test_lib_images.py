import pytest

from juniorguru.lib import images


@pytest.mark.parametrize('mimetype, expected', [
    (None, False),
    ('image/jpeg', True),
    ('application/octet-stream', False),
])
def test_is_image_mimetype(mimetype, expected):
    assert images.is_image_mimetype(mimetype) == expected
