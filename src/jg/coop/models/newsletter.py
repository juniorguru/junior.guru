import re
from datetime import datetime
from typing import Self

from peewee import CharField, DateField

from jg.coop.lib.text import remove_emoji
from jg.coop.models.base import BaseModel


class NewsletterIssue(BaseModel):
    id = CharField(primary_key=True)
    slug = CharField(unique=True)
    publish_on = DateField(unique=True)
    subject = CharField()
    content_html_raw = CharField()

    @property
    def content_html(self) -> str:
        return process_content_html(self.content_html_raw)

    @classmethod
    def from_buttondown(cls, data: dict) -> Self:
        return cls(
            id=data["id"],
            slug=data["slug"],
            publish_on=datetime.fromisoformat(data["publish_date"]).date(),
            subject=data["subject"],
            content_html_raw=data["body"],
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls) -> list[Self]:
        return list(cls.select().order_by(cls.publish_on.desc()))


def process_content_html(content_html: str) -> str:
    # remove double <br>
    content_html = re.sub(r"<br>\s*<br>", "<br>", content_html)

    # strip emoji from <h2> and <h3>
    content_html = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, content_html)
    content_html = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, content_html)

    return content_html


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
