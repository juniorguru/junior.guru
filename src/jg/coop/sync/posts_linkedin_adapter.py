"""Optional field mapping for the LinkedIn posts sync.

The sync still reads the last successful dataset of supreme_coder/linkedin-post.
Pass johnvc/linkedin-posts-api to fill postedAtISO and url from that actor's fields.
"""

from __future__ import annotations

from typing import Any

DEFAULT_LINKEDIN_POSTS_ACTOR = "supreme_coder/linkedin-post"
OPTIONAL_LINKEDIN_POSTS_ACTOR = "johnvc/linkedin-posts-api"


def accept_linkedin_posts(actor_name: str, posts: list[Any]) -> list[Any]:
    if actor_name != OPTIONAL_LINKEDIN_POSTS_ACTOR:
        return posts
    accepted: list[dict] = []
    for post in posts:
        if not isinstance(post, dict) or post.get("result_type") != "post":
            continue
        posted_at = post.get("postedAtISO") or post.get("datePosted")
        url = post.get("url") or post.get("postUrl")
        if not posted_at or not url:
            continue
        row = dict(post)
        row["postedAtISO"] = posted_at
        row["url"] = url
        accepted.append(row)
    return accepted
