from typing import Iterable, Self

from peewee import BooleanField, CharField, DateField, IntegerField

from jg.coop.models.base import BaseModel, JSONField


class Page(BaseModel):
    src_uri = CharField(unique=True)
    dest_uri = CharField(unique=True)
    title = CharField()
    size = IntegerField(null=True)
    notes_size = IntegerField(null=True)
    noindex = BooleanField(default=False, index=True)
    date = DateField(null=True)
    thumbnail_path = CharField(null=True)
    thumbnail_title = CharField(null=True)
    mainnav_name = CharField()
    nav_name = CharField(null=True)
    nav_sort_key = IntegerField(null=True)
    stages = JSONField(null=True, index=True)
    meta = JSONField(default=dict)

    @classmethod
    def from_meta(
        cls,
        src_uri: str,
        dest_uri: str,
        meta_data: dict,
    ):
        return cls(
            src_uri=src_uri,
            dest_uri=dest_uri,
            title=meta_data["title"],
            thumbnail_title=meta_data.get("thumbnail_title"),
            noindex=meta_data.get("noindex", False),
            date=meta_data.get("date"),
            stages=sorted(set(meta_data["stages"])) if "stages" in meta_data else None,
            meta=meta_data,
        )

    @property
    def absolute_url(self) -> str:
        return f"https://junior.guru/{self.dest_uri.removesuffix('index.html')}"

    def to_card(self) -> dict:
        if self.src_uri.startswith("stories/"):
            return dict(
                title=self.title,
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
            .where(
                cls.nav_name.is_null(False),
                cls.noindex == False,  # noqa: E712
                stages.c.value == slug,
            )
            .order_by(cls.nav_sort_key)
        )

    @classmethod
    def stage_todo_listing(cls, slug: str) -> Iterable[Self]:
        stages = cls.stages.children().alias("stages")
        return (
            cls.listing()
            .from_(cls, stages)
            .where(
                cls.noindex == True,  # noqa: E712
                stages.c.value == slug,
            )
            .order_by(cls.title)
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
