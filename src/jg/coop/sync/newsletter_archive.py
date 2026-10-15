import json
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

import click
from lxml import html

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.template_filters import nplurals
from jg.coop.models.base import db
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


MEETUPS_HEADING = "Srazy, konference a jiné akce"

STORIES_HEADING = "Nepřibarvené příběhy juniorů"

RECORDINGS_HEADING = "Záznamy z online akcí"

STORIES_URL_PREFIX = "junior.guru/stories/"

EVENTS_URL_PREFIX = "junior.guru/events/"

SUBJECT_PERIOD_RE = re.compile(r"^(\w+ \d{4}) ")


@cli.sync_command()
@click.option(
    "--archive-dir",
    default=Path("src/jg/coop/data/newsletter"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@click.option(
    "--today", default=lambda: date.today().isoformat(), type=date.fromisoformat
)
@db.connection_context()
@async_command
async def main(archive_dir: Path, today: date):
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
            newsletter_issue.subject, newsletter_issue.content_html
        )
        newsletter_issue.save()
        logger.info(f"Saved as {newsletter_issue!r}")
    logger.info(f"Done, {NewsletterIssue.count()} issues saved")


def get_issue_description(subject: str, content_html: str) -> str:
    if not (match := SUBJECT_PERIOD_RE.match(subject)):
        raise ValueError(f"Unexpected newsletter subject: {subject!r}")
    period = match.group(1).lower()
    meetups_count = get_meetups_count(content_html)
    meetups = f"{meetups_count} {nplurals(meetups_count, 'akce', 'akce', 'akcí')}"
    return (
        f"Shrnutí pro juniory v IT za {period}: "
        f"{meetups} kam přijít, "
        f"příběh „{get_story_headline(content_html)}“, "
        f"záznam z akce „{get_recording_title(content_html)}“"
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


def get_story_headline(
    content_html: str,
    heading: str = STORIES_HEADING,
    url_prefix: str = STORIES_URL_PREFIX,
) -> str:
    return get_linked_item_text(content_html, heading, url_prefix)


def get_recording_title(
    content_html: str,
    heading: str = RECORDINGS_HEADING,
    url_prefix: str = EVENTS_URL_PREFIX,
) -> str:
    text = get_linked_item_text(content_html, heading, url_prefix)
    try:
        return text.split(": ", 1)[1]
    except IndexError:
        raise ValueError(f"No speaker and title in {text!r}")


def get_linked_item_text(content_html: str, heading: str, url_prefix: str) -> str:
    """
    Returns text of the first list item linking to the given URL prefix,
    where items are lines like '▪️ Text – <a href="...">Link</a><br>'
    """
    for el in get_section(content_html, heading):
        for link in el.cssselect(f'a[href*="{url_prefix}"]'):
            text = get_line_before(link)
            return " ".join(text.replace("▪️", "").split()).rstrip(" –")
    raise ValueError(f"No {url_prefix!r} link in the {heading!r} section")


def get_line_before(el: html.HtmlElement) -> str:
    parent = el.getparent()
    text = parent.text or ""
    for sibling in parent:
        if sibling is el:
            return text
        if sibling.tag == "br":
            text = sibling.tail or ""
        else:
            text += sibling.text_content() + (sibling.tail or "")
    raise ValueError("Element not found in its parent")


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
