from typing import Iterable, Self

from peewee import BooleanField, CharField, DateField, IntegerField, TextField

from juniorguru.models.base import BaseModel, JSONField


class Page(BaseModel):
    src_uri = CharField(unique=True)
    dest_uri = CharField(unique=True)
    # title = CharField()
    # name = CharField(null=True)
    meta = JSONField(default=dict)
    size = IntegerField(null=True)
    notes = TextField(null=True)
    wip = BooleanField(default=False, index=True)
    date = DateField(null=True)
    thumbnail_path = CharField(null=True)
    stages = JSONField(null=True, index=True)

    @property
    def notes_size(self) -> int:
        return len(self.notes) if self.notes else 0

    def to_card(self) -> dict:
        if self.src_uri.startswith("stories/"):
            return dict(
                title=self.meta["title"],
                url=self.src_uri,
                image_path=self.meta["interviewee_avatar_path"],
                image_alt=self.meta["interviewee"],
                subtitle=self.meta["interviewee"],
                date=self.date,
            )
        raise ValueError(f"Unsupported page type: {self.src_uri}")

    @classmethod
    def get_by_src_uri(cls, src_uri) -> Self:
        return cls.get(cls.src_uri == src_uri)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select()

    @classmethod
    def stage_listing(cls, slug: str) -> Iterable[Self]:
        stages = cls.stages.children().alias("stages")
        return (
            cls.listing()
            .from_(cls, stages)
            .where(cls.wip == False, stages.c.value == slug)
        )

    @classmethod
    def handbook_listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .where(cls.src_uri.startswith("handbook/"))
            .order_by(cls.src_uri)
        )

    @classmethod
    def handbook_total_size(cls) -> int:
        return sum([page.size for page in cls.handbook_listing()])

    @classmethod
    def stories_listing(cls) -> Iterable[Self]:
        return (
            cls.select()
            .where(cls.src_uri.startswith("stories/"))
            .order_by(cls.date.desc())
        )


class LegacyThumbnail(BaseModel):  # can be deleted once Flask is gone
    url = CharField(index=True, unique=True)
    image_path = CharField()

    @classmethod
    def image_path_by_url(cls, url: str) -> str:
        return cls.get(cls.url == url).image_path
