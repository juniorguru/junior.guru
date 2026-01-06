#!/usr/bin/env python3
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.newsletter import NewsletterIssue
from jg.coop.models.podcast import PodcastEpisode
from jg.coop.models.topic import Topic


REQUIRED_TOPICS = ["adventofcode", "javascript", "python"]

REQUIRED_EVENTS = [
    {
        "id": 18,
        "title": "Mental health in IT",
        "start_at": datetime(2022, 2, 15, 18, 0, 0),
        "duration_s": 3600,
        "public_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "id": 36,
        "title": "Doubts in IT",
        "start_at": datetime(2023, 5, 10, 18, 0, 0),
        "duration_s": 4200,
        "public_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "id": 45,
        "title": "CV for juniors",
        "start_at": datetime(2022, 4, 1, 18, 0, 0),
        "duration_s": 3 * 60 * 60 + 30 * 60,
        "public_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
]

PLANNED_MIN_COUNT = 2
ARCHIVE_MIN_COUNT = 3


def ensure_event(event_id, title, start_at, duration_s=3600, public_url=None):
    if Event.select().where(Event.id == event_id).exists():
        return
    Event.create(
        id=event_id,
        title=title,
        start_at=start_at,
        end_at=start_at + timedelta(seconds=duration_s),
        description="Sample event for local build.",
        short_description="Sample event.",
        bio="Sample bio.",
        bio_name="Sample speaker",
        bio_title="Speaker",
        bio_links=["https://example.com"],
        avatar_path="avatars-participants/honza-javorek.jpg",
        poster_path="club.png",
        plain_poster_path="club.png",
        public_recording_url=public_url,
        public_recording_duration_s=duration_s if public_url else None,
    )


def ensure_podcast_episode_one():
    if PodcastEpisode.select().where(PodcastEpisode.number == 1).exists():
        return
    podcast_path = Path("src/jg/coop/data/podcast.yml")
    items = yaml.safe_load(podcast_path.read_text())
    item = next(i for i in items if i.get("number") == 1)
    media_slug = f"{item['number']:04d}"
    PodcastEpisode.create(
        number=item["number"],
        publish_on=date.fromisoformat(item["publish_on"]),
        title=item["title"],
        guest_name=item.get("guest_name"),
        guest_has_feminine_name=None,
        guest_affiliation=item.get("guest_affiliation"),
        image_path=item["image_path"],
        description=item["description"],
        media_slug=media_slug,
        media_url=f"https://podcast.junior.guru/episodes/{media_slug}.mp3",
        media_size=item["media_size"],
        media_type="audio/mpeg",
        media_duration_s=item["media_duration_s"],
        poster_path=None,
    )


def ensure_newsletter_issue():
    if NewsletterIssue.select().count() > 0:
        return
    NewsletterIssue.create(
        buttondown_id="local-1",
        slug="local-issue",
        published_on=date(2024, 1, 1),
        subject_raw="Local issue",
        subject="Local issue",
        content_html="<p>Local issue content.</p>",
        reading_time=1,
        canonical_url=None,
        thumbnail_url=None,
    )


def ensure_course_providers():
    redirects = yaml.safe_load(Path("src/jg/coop/data/redirects.yml").read_text())
    slugs = sorted(
        {
            Path(entry["to_doc"]).stem
            for entry in redirects.get("registry", [])
            if isinstance(entry.get("to_doc"), str)
            and entry["to_doc"].startswith("courses/")
        }
    )
    for slug in slugs:
        Topic.get_or_create(name=slug)
        CourseProvider.get_or_create(
            slug=slug,
            defaults={
                "name": slug.replace("-", " ").title(),
                "url": f"https://example.com/{slug}",
                "edit_url": f"https://example.com/edit/{slug}",
                "page_title": f"Courses by {slug.replace('-', ' ').title()}",
                "page_description": f"Local stub page for {slug}.",
                "page_lead": f"Local stub info for {slug.replace('-', ' ').title()}.",
            },
        )


def main():
    with db:
        for name in REQUIRED_TOPICS:
            Topic.get_or_create(name=name)

        for event in REQUIRED_EVENTS:
            ensure_event(
                event_id=event["id"],
                title=event["title"],
                start_at=event["start_at"],
                duration_s=event["duration_s"],
                public_url=event["public_url"],
            )

        planned_count = Event.planned_listing().count()
        archive_count = Event.archive_listing().count()

        for idx in range(max(0, PLANNED_MIN_COUNT - planned_count)):
            start_at = datetime(2030, 1, 10 + idx, 18, 0, 0)
            ensure_event(100 + idx, f"Planned event {idx + 1}", start_at)

        for idx in range(max(0, ARCHIVE_MIN_COUNT - archive_count)):
            start_at = datetime(2021, 1, 10 + idx, 18, 0, 0)
            ensure_event(200 + idx, f"Archived event {idx + 1}", start_at)

        ensure_podcast_episode_one()
        ensure_newsletter_issue()
        ensure_course_providers()

    print("Minimal seed complete.")


if __name__ == "__main__":
    main()
