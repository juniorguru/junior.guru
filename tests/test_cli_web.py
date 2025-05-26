from pathlib import Path

import pytest

from jg.coop.cli.web import resolve_path


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
