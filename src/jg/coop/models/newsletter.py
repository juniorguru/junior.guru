import re
from datetime import datetime
from typing import Self

from peewee import CharField, DateField, IntegerField

from jg.coop.lib.reading_time import reading_time
from jg.coop.lib.text import extract_text, remove_emoji
from jg.coop.models.base import BaseModel


class NewsletterIssue(BaseModel):
    buttondown_id = CharField(unique=True)
    slug = CharField(unique=True)
    published_on = DateField(unique=True)
    subject_raw = CharField()
    subject = CharField()
    content_html = CharField()
    content_html_raw = CharField()
    reading_time = IntegerField()

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
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls) -> list[Self]:
        return list(cls.select().order_by(cls.published_on.desc()))


def process_content_html(content_html: str) -> str:
    # remove double <br>
    content_html = re.sub(r"<br>\s*<br>", "<br>", content_html)

    # strip emoji from <h2> and <h3>
    content_html = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, content_html)
    content_html = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, content_html)

    return content_html


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
