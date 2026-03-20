from typing import Iterable, Self

from peewee import BooleanField, CharField, DateField, IntegerField, fn

from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubChannel, ClubMessage
from jg.coop.models.topic import TopicDiscussion


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

    @property
    def thumbnail_url(self) -> str | None:
        if self.thumbnail_path:
            return f"https://junior.guru/static/{self.thumbnail_path}"
        return None

    @classmethod
    def get_by_src_uri(cls, src_uri) -> Self:
        return cls.get(cls.src_uri == src_uri)

    @classmethod
    def listing(cls) -> Iterable[Self]:
        return cls.select()

    @classmethod
    def newsletter_listing(cls) -> Iterable[Self]:
        return (
            cls.listing()
            .where(cls.src_uri.startswith("news/"))
            .order_by(cls.date.desc())
        )

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

    def list_topic_discussions(self) -> Iterable[TopicDiscussion]:
        page_src_uris = TopicDiscussion.page_src_uris.children().alias("page_src_uris")
        return (
            TopicDiscussion.select()
            .from_(TopicDiscussion, page_src_uris)
            .where(page_src_uris.c.value == self.src_uri)
            .order_by(TopicDiscussion.monthly_letters_count.desc())
        )

    def list_related_channels(self) -> Iterable[ClubChannel]:
        channel_ids = [
            channel_id
            for topic_discussion in self.list_topic_discussions()
            for channel_id in topic_discussion.channel_ids
        ]
        if not channel_ids:
            return []
        return (
            ClubChannel.select()
            .where(ClubChannel.id.in_(channel_ids))
            .order_by(fn.czech_sort(ClubChannel.name))
        )

    def list_related_messages(
        self,
        min_content_size: int = 50,
        max_content_size: int = 200,
        chars_blocklist: str = "@",
    ) -> Iterable[ClubMessage]:
        channel_ids = [
            channel_id
            for topic_discussion in self.list_topic_discussions()
            for channel_id in topic_discussion.channel_ids
        ]
        if not channel_ids:
            return []
        raise NotImplementedError()
        # query = (
        #     ClubMessage.select()
        #     .where(
        #         ClubMessage.parent_channel_id.in_(channel_ids)
        #         | ClubMessage.channel_id.in_(channel_ids)
        #     )
        #     .where(ClubMessage.content_size >= min_content_size)
        #     .where(ClubMessage.content_size <= max_content_size)
        #     .order_by(ClubMessage.upvotes_count.desc(), ClubMessage.created_at.desc())
        # )
        # for char in chars_blocklist:
        #     query = query.where(~ClubMessage.content.contains(char))
        # return query

    @property
    def related_channels_monthly_size(self) -> int:
        return sum(
            topic_discussion.monthly_letters_count
            for topic_discussion in self.list_topic_discussions()
        )

    def list_related(self) -> list[Self]:
        # unique
        pages_by_uri = {}
        for stage_slug in self.stages or []:
            for related_page in self.stage_listing(stage_slug):
                pages_by_uri[related_page.src_uri] = related_page

        # don't include the page itself in the related listing
        pages_by_uri.pop(self.src_uri, None)

        return sorted(
            pages_by_uri.values(),
            key=lambda related_page: (
                related_page.nav_sort_key is None,
                related_page.nav_sort_key,
            ),
        )
