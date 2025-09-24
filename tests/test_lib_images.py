import pytest

from jg.coop.lib.images import _get_source_paths, is_image_mimetype


@pytest.mark.parametrize(
    "mimetype, expected",
    [
        (None, False),
        ("image/jpeg", True),
        ("application/octet-stream", False),
    ],
)
def test_is_image_mimetype(mimetype, expected):
    assert is_image_mimetype(mimetype) == expected


def test_get_source_paths():
    metafile = {
        "inputs": {
            "src/jg/coop/image_templates/event.scss": {"bytes": 9547, "imports": []},
            "node_modules/@fontsource/inter/files/inter-cyrillic-ext-400-normal.woff2": {
                "bytes": 10216,
                "imports": [],
            },
            "node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2?24e3eb84d0bcaf83d77f904c78ac1f47": {
                "bytes": 130396,
                "imports": [],
            },
            "src/jg/coop/image_templates/thumbnail.scss": {
                "bytes": 1239348,
                "imports": [
                    {
                        "path": "node_modules/@fontsource/inter/files/inter-cyrillic-ext-400-normal.woff2",
                        "kind": "url-token",
                        "original": "../../../node_modules/@fontsource/inter/files/inter-cyrillic-ext-400-normal.woff2",
                    },
                    {
                        "path": "node_modules/@fontsource/inter/files/inter-cyrillic-400-normal.woff",
                        "kind": "url-token",
                        "original": "../../../node_modules/@fontsource/inter/files/inter-cyrillic-400-normal.woff",
                    },
                ],
            },
        }
    }

    assert _get_source_paths(metafile) == [
        "node_modules/@fontsource/inter/files/inter-cyrillic-400-normal.woff",
        "node_modules/@fontsource/inter/files/inter-cyrillic-ext-400-normal.woff2",
        "node_modules/bootstrap-icons/font/fonts/bootstrap-icons.woff2",
        "src/jg/coop/image_templates/event.scss",
        "src/jg/coop/image_templates/thumbnail.scss",
    ]
