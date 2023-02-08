import re
from urllib.parse import urlparse

from peewee import CharField, DateField

from juniorguru.models.base import BaseModel, JSONField


class Story(BaseModel):
    url = CharField()
    date = DateField(index=True)
    title = CharField()
    image_path = CharField()
    tags = JSONField(default=list)

    @property
    def publisher(self):
        return re.sub(r'^www\.', '', urlparse(self.url).netloc).lower()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.date.desc())

    @classmethod
    def tag_listing(cls, tag):
        tags = cls.tags.children().alias('tags')
        return cls.listing() \
            .from_(cls, tags) \
            .where(tags.c.value == tag)

    @classmethod
    def tags_mapping(cls):
        mapping = {}
        for story in cls.listing():
            for tag in story.tags:
                mapping.setdefault(tag, [])
                mapping[tag].append(story)
        return mapping
