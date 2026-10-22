"""Offline coverage for the optional LinkedIn posts field mapping."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "jg"
    / "coop"
    / "sync"
    / "posts_linkedin_adapter.py"
)
_SPEC = importlib.util.spec_from_file_location("posts_linkedin_adapter", _PATH)
assert _SPEC and _SPEC.loader
adapter = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(adapter)


def test_default_actor_rows_are_unchanged():
    posts = [{"postedAtISO": "2026-01-02T03:04:05Z", "url": "https://example.com/post", "error": None}]
    assert adapter.accept_linkedin_posts(adapter.DEFAULT_LINKEDIN_POSTS_ACTOR, posts) is posts
    assert adapter.accept_linkedin_posts("other/actor", posts) is posts


def test_optional_actor_fills_posted_at_and_url_and_drops_error_rows():
    rows = adapter.accept_linkedin_posts(
        adapter.OPTIONAL_LINKEDIN_POSTS_ACTOR,
        [
            {
                "result_type": "post",
                "postId": "",
                "postUrl": "https://www.linkedin.com/posts/example",
                "datePosted": "2026-01-02T03:04:05.000Z",
                "text": "",
                "authorName": "",
                "authorUrl": "",
            },
            {"result_type": "error", "error_type": "CollectionError", "error_message": "none"},
            {"result_type": "post", "datePosted": "", "postUrl": ""},
        ],
    )
    assert rows == [
        {
            "result_type": "post",
            "postId": "",
            "postUrl": "https://www.linkedin.com/posts/example",
            "datePosted": "2026-01-02T03:04:05.000Z",
            "text": "",
            "authorName": "",
            "authorUrl": "",
            "postedAtISO": "2026-01-02T03:04:05.000Z",
            "url": "https://www.linkedin.com/posts/example",
        }
    ]
