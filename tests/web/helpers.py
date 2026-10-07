"""
Helpers for creating sample data for the browser tests
"""

from datetime import date

from jg.coop.lib.location import REGIONS
from jg.coop.models.club import ClubUser
from jg.coop.models.job import DiscordJob, ListedJob


def create_job(regions: list[str] | None = None, **kwargs) -> ListedJob:
    title = kwargs.pop("title", "Junior Developer")
    if regions:
        kwargs["locations"] = [create_location(region) for region in regions]
    return ListedJob.create(
        **{
            "title": title,
            "posted_on": date(2026, 1, 1),
            "lang": "cs",
            "description_html": f"<p>{title}</p>",
            "description_text": title,
            "description_discord": title,
            "url": f"https://example.com/jobs/{ListedJob.select().count() + 1}",
            "company_name": "První Programátorská, a.s.",
            "company_logo_path": "logos-jobs/unknown.webp",
            **kwargs,
        }
    )


def create_location(region: str) -> dict[str, str]:
    if region not in REGIONS:
        raise ValueError(f"Unknown region: {region}")
    return {"raw": region, "place": region, "region": region, "country_code": "CZ"}


def create_discord_job(**kwargs) -> DiscordJob:
    author, _ = ClubUser.get_or_create(
        id=1, defaults={"display_name": "Kuře Žluté", "mention": "<@1>"}
    )
    number = DiscordJob.select().count() + 1
    return DiscordJob.create(
        **{
            "title": "Junior Developer from Discord",
            "author": author,
            "posted_on": date(2026, 1, 1),
            "description_discord": "Junior Developer from Discord",
            "url": f"https://discord.com/channels/1/2/{number}",
            "upvotes_count": 0,
            "comments_count": 0,
            **kwargs,
        }
    )
