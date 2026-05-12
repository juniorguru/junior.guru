from pathlib import Path
from textwrap import dedent

import pytest
from bs4 import BeautifulSoup

from jg.coop.cli.web import _cache_bust_urls, hash_file, resolve_path


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

    soup = BeautifulSoup(html_text, "html.parser")
    _cache_bust_urls(soup, output_path, html_path)
    result = str(soup)

    assert f"../static/css/index.css?hash={hash_file(css_path)}" in result
    assert f"../static/js/index.js?hash={hash_file(js_path)}" in result
