import re
from datetime import datetime
from typing import Iterable, Self

from peewee import CharField, DateField, IntegerField

from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.text import extract_text, remove_emoji
from jg.coop.models.base import BaseModel
from jg.coop.models.page import Page


class NewsletterIssue(BaseModel):
    buttondown_id = CharField(unique=True)
    slug = CharField(unique=True)
    published_on = DateField(unique=True)
    subject_raw = CharField()
    subject = CharField()
    content_html = CharField()
    content_html_raw = CharField()
    reading_time = IntegerField()
    canonical_url = CharField(null=True)
    thumbnail_url = CharField(null=True)

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
        return cls(
            buttondown_id=data["id"],
            slug=data["slug"],
            published_on=datetime.fromisoformat(data["publish_date"]).date(),
            subject_raw=data["subject"],
            subject=remove_emoji(data["subject"]),
            content_html=process_content_html(data["body"]),
            content_html_raw=data["body"],
            reading_time=reading_time(len(extract_text(data["body"]))),
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


def process_content_html(content_html: str) -> str:
    # remove double <br>
    content_html = re.sub(r"<br>\s*<br>", "<br>", content_html)

    # strip emoji from <h2> and <h3>
    content_html = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, content_html)
    content_html = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, content_html)

    return content_html


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
