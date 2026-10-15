import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

import click
from lxml import html
from mkdocs.utils.meta import get_data as parse_document

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.template_filters import nplurals
from jg.coop.models.base import db
from jg.coop.models.event import Event
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


MEETUPS_HEADING = "Srazy, konference a jiné akce"

STORIES_HEADING = "Nepřibarvené příběhy juniorů"

RECORDINGS_HEADING = "Záznamy z online akcí"

STORIES_URL_PREFIX = "junior.guru/stories/"

EVENTS_URL_PREFIX = "junior.guru/events/"

SUBJECT_PERIOD_RE = re.compile(r"^(\w+ \d{4}) ")


@cli.sync_command(dependencies=["events"])
@click.option(
    "--archive-dir",
    default=Path("src/jg/coop/data/newsletter"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@click.option(
    "--stories-dir",
    default=Path("src/jg/coop/web/docs/stories"),
    type=click.Path(path_type=Path, exists=True, file_okay=False),
)
@click.option(
    "--today", default=lambda: date.today().isoformat(), type=date.fromisoformat
)
@db.connection_context()
@async_command
async def main(archive_dir: Path, stories_dir: Path, today: date):
    archive_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Newsletter archive: {archive_dir}")

    logger.info("Fetching newsletter issues from Buttondown")
    async with ButtondownAPI() as api:
        async for email_data in api.get_emails_before(today):
            logger.info(f"Fetched {email_data['absolute_url']}")
            published_on = datetime.fromisoformat(email_data["publish_date"]).date()
            path = archive_dir / f"{published_on}.json"
            path.write_text(json.dumps(email_data, ensure_ascii=False, indent=2) + "\n")
            logger.info(f"Archived as {path}")

    logger.info("Tidying up JSON files")
    subprocess.run(["npx", "oxfmt", str(archive_dir)], check=True)

    logger.info("Saving published issues to database")
    NewsletterIssue.drop_table()
    NewsletterIssue.create_table()
    for path in sorted(archive_dir.glob("*.json")):
        logger.info(f"Reading {path}")
        data = json.loads(path.read_text())
        newsletter_issue = NewsletterIssue.from_buttondown(data)
        newsletter_issue.description = get_issue_description(
            newsletter_issue.subject,
            get_meetups_count(newsletter_issue.content_html),
            get_story_interviewee(
                stories_dir, get_story_slug(newsletter_issue.content_html)
            ),
            get_event_title(get_recording_event_id(newsletter_issue.content_html)),
        )
        newsletter_issue.save()
        logger.info(f"Saved as {newsletter_issue!r}")
    logger.info(f"Done, {NewsletterIssue.count()} issues saved")


def get_story_interviewee(stories_dir: Path, slug: str) -> str:
    _, meta = parse_document((stories_dir / f"{slug}.md").read_text())
    return meta["interviewee"]


def get_event_title(event_id: int) -> str:
    return Event.get_by_id(event_id).title


def get_issue_description(
    subject: str, meetups_count: int, interviewee: str, recording_title: str
) -> str:
    if not (match := SUBJECT_PERIOD_RE.match(subject)):
        raise ValueError(f"Unexpected newsletter subject: {subject!r}")
    period = match.group(1).lower()
    meetups = f"{meetups_count} {nplurals(meetups_count, 'akce', 'akce', 'akcí')}"
    return (
        f"Shrnutí pro juniory v IT za {period}: "
        f"{meetups} kam přijít, "
        f"{interviewee} o své cestě do IT, "
        f"záznam z akce „{' '.join(recording_title.split())}“"
    )


def get_meetups_count(content_html: str, heading: str = MEETUPS_HEADING) -> int:
    paragraphs = [
        el
        for el in get_section(content_html, heading)
        if el.tag == "p"
        and not (el.text or "").strip()
        and el[:1]
        and el[0].tag == "strong"
    ]
    if not paragraphs:
        raise ValueError(f"No meetups in the {heading!r} section")
    return len(paragraphs)


def get_story_slug(
    content_html: str,
    heading: str = STORIES_HEADING,
    url_prefix: str = STORIES_URL_PREFIX,
) -> str:
    return get_linked_value(content_html, heading, url_prefix, r"[\w-]+")


def get_recording_event_id(
    content_html: str,
    heading: str = RECORDINGS_HEADING,
    url_prefix: str = EVENTS_URL_PREFIX,
) -> int:
    return int(get_linked_value(content_html, heading, url_prefix, r"\d+"))


def get_linked_value(
    content_html: str, heading: str, url_prefix: str, value_pattern: str
) -> str:
    url_re = re.compile(rf"{re.escape(url_prefix)}({value_pattern})")
    for el in get_section(content_html, heading):
        for link in el.cssselect(f'a[href*="{url_prefix}"]'):
            if match := url_re.search(link.get("href")):
                return match.group(1)
    raise ValueError(f"No {url_prefix!r} link in the {heading!r} section")


def get_section(content_html: str, heading: str) -> list[html.HtmlElement]:
    root = html.fragment_fromstring(content_html, create_parent="div")
    for h2 in root.cssselect("h2"):
        if h2.text_content().strip() == heading:
            section = []
            for el in h2.itersiblings():
                if el.tag == "h2":
                    break
                section.append(el)
            return section
    raise ValueError(f"Section {heading!r} not found in the newsletter issue")
