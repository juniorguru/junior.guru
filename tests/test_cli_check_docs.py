from pathlib import Path

import pytest

from jg.coop.cli.check_docs import normalize_link


OUTPUT_PATH = Path("public")

DOC_PATH = OUTPUT_PATH / "jobs" / "index.html"


@pytest.mark.parametrize(
    "link, expected",
    [
        ("/club/", "/club/"),
        ("/club", "/club/"),
        ("/club/#pricing", "/club/#pricing"),
        ("#pricing", "/jobs/#pricing"),
        ("/club/?utm_source=jobs-teaser&utm_medium=web", "/club/"),
        ("/club/?utm_source=jobs-teaser#pricing", "/club/#pricing"),
    ],
)
def test_normalize_link(link: str, expected: str):
    assert normalize_link(OUTPUT_PATH, DOC_PATH, link) == expected
