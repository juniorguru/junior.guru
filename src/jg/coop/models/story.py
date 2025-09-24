import re
from urllib.parse import urlparse

from peewee import CharField, DateField

from jg.coop.models.base import BaseModel, JSONField


class Story(BaseModel):
    url = CharField()
    date = DateField(index=True)
    title = CharField()
    name = CharField()
    image_path = CharField()
    tags = JSONField(default=list)

    @property
    def publisher(self) -> str:
        if "web.archive.org" in self.url:
            url = re.sub(r"^https?://(www\.)?web\.archive\.org/web/\d+/", "", self.url)
        else:
            url = self.url
        return re.sub(r"^www\.", "", urlparse(url).netloc).lower()

    def to_card(self) -> dict:
        return dict(
            title=self.title,
            url=self.url,
            image_path=self.image_path,
            image_alt=self.name,
            subtitle=self.name,
            date=self.date,
            external=True,
        )

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.date.desc())

    @classmethod
    def tag_listing(cls, tag):
        tags = cls.tags.children().alias("tags")
        return cls.listing().from_(cls, tags).where(tags.c.value == tag)

    @classmethod
    def tags_mapping(cls) -> dict:
        mapping = {}
        for story in cls.listing():
            for tag in story.tags:
                mapping.setdefault(tag, [])
                mapping[tag].append(story)
        return mapping
