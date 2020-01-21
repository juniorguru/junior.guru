import re
from urllib.parse import urlparse

from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


class Story(BaseModel):
    url = CharField()
    date = DateTimeField(index=True)
    title = CharField()
    image_path = CharField()

    @property
    def publisher(self):
        return re.sub(r'^www\.', '', urlparse(self.url).netloc).lower()

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.date.desc())
