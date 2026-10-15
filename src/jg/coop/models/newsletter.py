from collections.abc import Iterable
from datetime import datetime
from typing import Self

from peewee import CharField, DateField, IntegerField

from jg.coop.lib.newsletter_content import parse_newsletter
from jg.coop.lib.text import remove_emoji
from jg.coop.models.base import BaseModel
from jg.coop.models.page import Page


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
        content = parse_newsletter(data["body"])
        subject = remove_emoji(data["subject"])
        return cls(
            buttondown_id=data["id"],
            slug=data["slug"],
            published_on=datetime.fromisoformat(data["publish_date"]).date(),
            subject_raw=data["subject"],
            subject=subject,
            content_html=content.html,
            reading_time=content.reading_time,
            canonical_url=data.get("canonical_url") or None,
            thumbnail_url=data.get("image") or None,
            description=content.get_description(subject),
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
