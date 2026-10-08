"""
Helpers for creating sample data for the browser tests
"""

from datetime import date

from playwright.sync_api import Page, expect

from jg.coop.lib.location import REGIONS
from jg.coop.models.candidate import Candidate, CandidateProject
from jg.coop.models.club import ClubUser
from jg.coop.models.job import DiscordJob, ListedJob, SubmittedJob


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


def hide_subscribe_box(page: Page) -> None:
    """
    Hides the subscribe box, which is fixed to the bottom of the window,
    so on the short test pages it covers whatever is below the first job

    The box hides when clicked, but the click also opens its link in a new tab,
    so the tab gets closed.
    """
    subscribe = page.locator(".jobs-subscribe")
    with page.context.expect_page() as new_page_info:
        subscribe.click()
    new_page_info.value.close()
    expect(subscribe).to_be_hidden()


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


def create_submitted_job(id: str = "abc123", **kwargs) -> ListedJob:
    title = kwargs.pop("title", "Junior Developer")
    submitted_job = SubmittedJob.create(
        **{
            "id": id,
            "title": title,
            "posted_on": date(2026, 1, 1),
            "expires_on": date(2026, 12, 31),
            "lang": "cs",
            "description_html": f"<p>{title}</p>",
            "description_text": title,
            "url": f"https://junior.guru/jobs/{id}/",
            "company_name": "První Programátorská, a.s.",
            "company_url": "https://example.com",
            **kwargs,
        }
    )
    job = submitted_job.to_listed()
    job.company_logo_path = "logos-jobs/unknown.webp"
    job.save()
    return job


def create_candidate(regions: list[str] | None = None, **kwargs) -> Candidate:
    name = kwargs.pop("name", "Kuře Žluté")
    username = kwargs.pop(
        "github_username", f"candidate{Candidate.select().count() + 1}"
    )
    if regions:
        kwargs["location_fuzzy"] = {
            "locations": [create_location(region) for region in regions],
            "is_universal": False,
        }
    if not kwargs.get("is_ready", True):
        number = Candidate.select().count() + 1
        kwargs.setdefault(
            "report_url", f"https://github.com/juniorguru/eggtray/issues/{number}"
        )
    return Candidate.create(
        **{
            "github_username": username,
            "github_url": f"https://github.com/{username}",
            "name": name,
            "avatar_url": f"https://avatars.githubusercontent.com/{username}",
            "avatar_is_default": False,
            "avatar_path": "chick-avatar.png",
            "is_ready": True,
            "is_member": False,
            "has_feminine_name": False,
            **kwargs,
        }
    )


def create_candidate_project(candidate: Candidate, **kwargs) -> CandidateProject:
    number = CandidateProject.select().count() + 1
    name = kwargs.pop("name", f"{candidate.github_username}/project{number}")
    return CandidateProject.create(
        **{
            "name": name,
            "candidate": candidate,
            "source_url": f"https://github.com/{name}",
            "priority": number,
            "start_on": date(2025, 1, 1),
            "end_on": date(2025, 3, 1),
            **kwargs,
        }
    )
