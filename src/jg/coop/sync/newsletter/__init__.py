import random
import time
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from pprint import pformat
from typing import Generator, Literal

import click
from jinja2 import Template
from lxml import html

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.discord_club import ClubChannelID
from jg.coop.lib.md import md
from jg.coop.lib.template_filters import thousands
from jg.coop.models.base import db
from jg.coop.models.club import ClubChannel, ClubMessage, ClubSummaryTopic, ClubUser
from jg.coop.models.course_provider import CourseProvider, CourseProviderGroup
from jg.coop.models.event import Event
from jg.coop.models.followers import Followers


MONTH_NAMES = [
    "Leden",
    "Únor",
    "Březen",
    "Duben",
    "Květen",
    "Červen",
    "Červenec",
    "Srpen",
    "Září",
    "Říjen",
    "Listopad",
    "Prosinec",
]


logger = loggers.from_path(__file__)


@cli.sync_command(
    dependencies=[
        "course-providers",
        "events",
        "pages",
        "podcast",
        "summary",
        "topics",
    ]
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Force creating even if there are already emails this month",
)
@click.option(
    "-o",
    "--open",
    "open_browser",
    is_flag=True,
    default=False,
    help="Open the created draft in browser",
)
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@db.connection_context()
@async_command
async def main(force: bool, open_browser: bool, today: date):
    # TODO change this so that it uses the date of last newsletter published
    # as the anchor date for stats calculation
    this_month = today.replace(day=1)
    prev_month = (this_month - timedelta(days=1)).replace(day=1)
    prev_prev_month = (prev_month - timedelta(days=1)).replace(day=1)

    async with ButtondownAPI() as api:
        logger.info(f"Checking existing emails since {this_month:%Y-%m-%d}")
        emails_count = (await api.get_emails_since(this_month))["count"]
        if emails_count:
            if force:
                logger.warning(
                    "Forcing email creation even though there are already emails this month!"
                )
            else:
                logger.warning(
                    "There are emails created this month. Skipping newsletter! Check https://buttondown.com/emails"
                )
                return

        logger.info("Preparing email data")
        month_name = MONTH_NAMES[today.month - 1]

        logger.debug("Preparing stats about subscribers")
        subscribers_count = Followers.get_latest("newsletter").count
        subscribers_new_count = (
            subscribers_count - Followers.breakdown(prev_prev_month)["newsletter"]
        )
        club_content_size = ClubMessage.content_size_by_month(prev_month)

        logger.debug("Preparing stats about jobs")
        jobs_count = 0
        jobs_tags_stats = Counter()
        for message in ClubMessage.forum_listing(ClubChannelID.JOBS):
            if message.created_at.date() >= prev_month:
                jobs_count += 1
                jobs_tags_stats.update(get_job_tags(message))
        jobs_tags_stats = jobs_tags_stats.most_common(20)

        logger.debug("Preparing stats about courses")
        cps_group, cps_items = CourseProvider.grouping()[0]
        cps_sponsors = cps_items if cps_group == CourseProviderGroup.HIGHLIGHTED else []
        cps_most_viewed = [
            cp
            for cp in CourseProvider.pageviews_listing("page_last_month_pageviews")
            if cp not in cps_sponsors
        ]
        course_providers = cps_sponsors + cps_most_viewed
        course_providers_by_mentions = list(
            CourseProvider.mentions_listing("mentions_last_month_count")
        )

        logger.debug("Preparing info about top club groups")
        club_groups = list(
            ClubMessage.forum_top_listing(ClubChannelID.GROUPS, prev_month)
        )

        logger.debug("Preparing info about top club diaries")
        club_diaries_threads = list(
            ClubMessage.forum_top_listing(ClubChannelID.DIARIES, prev_month)
        )
        club_diaries = [
            {
                "name": message.channel_name,
                "url": message.url,
                "author": get_initials(
                    ClubMessage.get_by_id(message.channel_id).author.display_name
                ),
            }
            for message in club_diaries_threads
        ]

        logger.debug("Preparing info about club creations")
        club_creations_threads = list(
            ClubMessage.forum_top_listing(ClubChannelID.CREATIONS, prev_month)
        )
        club_creations = [
            {
                "name": message.channel_name,
                "url": message.url,
                "author": get_initials(
                    ClubMessage.get_by_id(message.channel_id).author.display_name
                ),
            }
            for message in club_creations_threads
        ]

        logger.debug("Preparing info about club CVs")
        club_cv_reviews = []
        club_cv_threads = list(
            ClubMessage.forum_top_listing(ClubChannelID.CV_GITHUB_LINKEDIN, prev_month)
        )
        for message in club_cv_threads:
            thread = ClubChannel.get_by_id(message.channel_id)
            for review_type in get_cv_review_types(thread.tags):
                club_cv_reviews.append(
                    {
                        "type": review_type,
                        "url": message.url,
                        "author": get_initials(
                            ClubMessage.get_by_id(
                                message.channel_id
                            ).author.display_name
                        ),
                    }
                )

        logger.debug("Preparing events")
        events_planned = list(Event.planned_listing())
        events_archive = list(
            Event.archive_listing(has_recording=True, has_avatar=True)
        )
        event_last = events_archive[0]
        event_random = random.choice(list(events_archive[1:]))

        logger.debug("Rendering email body")
        template = Template(Path(__file__).with_name("newsletter.jinja").read_text())
        template_context = dict(
            club_content_size=thousands(club_content_size),
            club_creations=club_creations,
            club_cv_reviews=club_cv_reviews,
            club_diaries=club_diaries,
            club_groups=club_groups,
            course_providers_by_mentions=course_providers_by_mentions,
            course_providers=course_providers,
            event_last=event_last,
            event_random=event_random,
            events_planned=events_planned,
            jobs_count=jobs_count,
            jobs_tags_stats=jobs_tags_stats,
            members_count=ClubUser.members_count(),
            month_name=month_name,
            subscribers_count=subscribers_count,
            subscribers_new_count=subscribers_new_count,
            topics=ClubSummaryTopic.listing(),
        )
        logger.debug(f"Template context:\n{pformat(template_context)}")
        email_data = {
            "subject": f"{month_name} {today.year} ve světě IT juniorů 🐣",
            "body": template.render(template_context),
            "status": "draft",
        }
        logger.debug(f"Email data:\n{pformat(email_data)}")

        logger.info("Creating draft")
        if data := await api.create_draft(email_data):
            logger.info(
                f"Email created!\nEdit: https://buttondown.com/emails/{data['id']}\nPreview: {data['absolute_url']}"
            )
            if open_browser:
                time.sleep(1)
                click.launch(data["absolute_url"])


def get_job_tags(message: ClubMessage) -> set[str]:
    html_tree = html.fromstring(md(message.content))
    tags = set()
    for code in html_tree.xpath("//code"):
        text = code.text_content().strip()
        if text.startswith("#"):
            tags.add(text)
    return tags


def get_cv_review_types(
    tags: list[str],
) -> Generator[Literal["cv", "gh", "li"], None, None]:
    prefix = "zpětná vazba na"
    relevant_tags = [tag for tag in map(str.lower, tags) if tag.startswith(prefix)]
    return [tag.removeprefix(prefix).strip() for tag in relevant_tags]


def get_initials(name: str) -> str:
    parts = name.split()
    return "".join([f"{part[0]}." for part in parts])
