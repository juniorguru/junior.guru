import re
from collections.abc import Iterable
from datetime import datetime
from typing import Self

from lxml import html
from peewee import CharField, DateField, IntegerField

from jg.coop.lib.md import md
from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.template_filters import nplurals
from jg.coop.lib.text import extract_text, remove_emoji
from jg.coop.models.base import BaseModel
from jg.coop.models.page import Page


MEETUPS_HEADING = "Srazy, konference a jiné akce"

STORIES_HEADING = "Nepřibarvené příběhy juniorů"

RECORDINGS_HEADING = "Záznamy z online akcí"

STORIES_URL_PREFIX = "junior.guru/stories/"

EVENTS_URL_PREFIX = "junior.guru/events/"

SUBJECT_PERIOD_RE = re.compile(r"^(\w+ \d{4}) ")


class NewsletterIssue(BaseModel):
    buttondown_id = CharField(unique=True)
    slug = CharField(unique=True)
    published_on = DateField(unique=True)
    subject_raw = CharField()
    subject = CharField()
    content_html = CharField()
    reading_time = IntegerField()
    canonical_url = CharField(null=True)
    thumbnail_url = CharField(null=True)
    description = CharField()

    @property
    def absolute_url(self) -> str:
        return self.page.absolute_url

    @property
    def page(self) -> Page:
        return Page.get_by_src_uri(f"news/{self.slug}.md")

    def get_buttondown_updates(self) -> dict:
        updates = {}

        # Canonical URL
        if self.canonical_url != self.absolute_url:
            updates["canonical_url"] = self.absolute_url

        # Thumbnail
        page = self.page
        if self.thumbnail_url != page.thumbnail_url:
            updates["image"] = page.thumbnail_url

        return updates

    @classmethod
    def from_buttondown(cls, data: dict) -> Self:
        content_html = content_to_html(data["body"])
        return cls(
            buttondown_id=data["id"],
            slug=data["slug"],
            published_on=datetime.fromisoformat(data["publish_date"]).date(),
            subject_raw=data["subject"],
            subject=remove_emoji(data["subject"]),
            content_html=edit_content_html(content_html),
            reading_time=reading_time(len(extract_text(content_html))),
            canonical_url=data.get("canonical_url") or None,
            thumbnail_url=data.get("image") or None,
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select().order_by(cls.published_on.desc())

    @classmethod
    def latest(cls) -> Self:
        return cls.listing().get()


def content_to_html(content_raw: str) -> str:
    # Detect if it's Markdown or HTML. Markdown can contain tags,
    # so we need a heuristic. If the text contains Markdown links,
    # it's probably Markdown.
    if re.search(r"\[.*?\]\(.*?\)", content_raw):
        return md(content_raw)
    return content_raw


def edit_content_html(content_html: str) -> str:
    # remove double <br>
    content_html = re.sub(r"<br>\s*<br>", "<br>", content_html)

    # strip emoji from <h2> and <h3>
    content_html = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, content_html)
    content_html = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, content_html)

    # add trailing slash to course provider URLs to avoid redirects
    content_html = re.sub(
        r'(href="https://junior\.guru/courses/[\w-]+)(?=["?#])', r"\1/", content_html
    )

    return content_html


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


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
