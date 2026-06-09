from pathlib import Path
from textwrap import dedent

import pytest
from PIL import Image

from jg.coop.cli.web import (
    _cache_bust_urls,
    _fill_image_dimensions,
    hash_file,
    resolve_path,
)


@pytest.mark.parametrize(
    "html_path, url, expected",
    [
        (
            Path("public/jobs/liberec/index.html"),
            "/static/js/index.js",
            Path("public/static/js/index.js"),
        ),
        (
            Path("public/podcast/index.html"),
            "../static/js/index.js",
            Path("public/static/js/index.js"),
        ),
        (
            Path("public/podcast/index.html"),
            "../static/js/index.js?v=1#footer",
            Path("public/static/js/index.js"),
        ),
    ],
)
def test_resolve_path(html_path: Path, url: str, expected: Path):
    assert resolve_path(Path("public"), html_path, url) == expected.resolve()


def test_resolve_path_raises():
    with pytest.raises(ValueError):
        resolve_path(
            Path("public"),
            Path("public/jobs/liberec/index.html"),
            "https://example.com",
        )


def test_cache_bust_urls_adds_hashes(tmp_path: Path):
    output_path = tmp_path / "public"
    html_path = output_path / "jobs/index.html"
    css_path = output_path / "static/css/index.css"
    js_path = output_path / "static/js/index.js"

    html_path.parent.mkdir(parents=True, exist_ok=True)
    css_path.parent.mkdir(parents=True, exist_ok=True)
    js_path.parent.mkdir(parents=True, exist_ok=True)

    css_path.write_text("body { color: black; }")
    js_path.write_text("console.log('ok');")

    html_text = dedent(
        """
        <html>
        <head>
            <link rel="stylesheet" href="../static/css/index.css">
            <script defer src="../static/js/index.js"></script>
        </head>
        <body><p>Ahoj</p></body>
        </html>
        """
    )

    result = _cache_bust_urls(html_text, output_path, html_path)

    assert f"../static/css/index.css?hash={hash_file(css_path)}" in result
    assert f"../static/js/index.js?hash={hash_file(js_path)}" in result


def test_fill_image_dimensions_sets_actual_size(tmp_path: Path):
    output_path = tmp_path / "public"
    html_path = output_path / "jobs/index.html"
    image_path = output_path / "static/figures/example.png"

    html_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.new("RGB", (123, 45)) as image:
        image.save(image_path)

    html_text = dedent(
        """
        <html>
        <body>
            <figure class="figure">
                <img src="../static/figures/example.png" alt="Example" width="700" class="figure-img" loading="lazy">
            </figure>
        </body>
        </html>
        """
    )
    result = _fill_image_dimensions(html_text, output_path, html_path)

    assert result == dedent(
        """
        <html>
        <body>
            <figure class="figure">
                <img alt="Example" class="figure-img" height="45" loading="lazy" src="../static/figures/example.png" width="123">
            </figure>
        </body>
        </html>
        """
    )


def test_fill_image_dimensions_removes_xhtml_slash(tmp_path: Path):
    output_path = tmp_path / "public"
    html_path = output_path / "index.html"
    image_path = output_path / "static/icons/logo.png"

    html_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.new("RGB", (11, 22)) as image:
        image.save(image_path)

    html_text = '<img src="static/icons/logo.png" alt="Logo" />'
    result = _fill_image_dimensions(html_text, output_path, html_path)

    assert (
        result == '<img alt="Logo" height="22" src="static/icons/logo.png" width="11">'
    )
