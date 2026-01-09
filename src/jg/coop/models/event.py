import itertools
import json
import math
from datetime import UTC, datetime
import random
from typing import Iterable, Self
from zoneinfo import ZoneInfo

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from jg.coop.lib.charts import month_range, ttm_range
from jg.coop.lib.discord_club import CLUB_GUILD_ID, ClubChannelID, parse_discord_link
from jg.coop.lib.md import strip_links
from jg.coop.lib.youtube import get_youtube_url, parse_youtube_id
from jg.coop.models.base import BaseModel, JSONField
from jg.coop.models.club import ClubMessage, ClubUser


class Event(BaseModel):
    title = CharField()
    start_at = DateTimeField(index=True)
    end_at = DateTimeField()
    description = TextField()
    short_description = TextField(null=True)
    bio = TextField()
    avatar_path = CharField(default="chick-avatar.png")
    bio_name = TextField()
    bio_title = TextField(null=True)
    bio_links = JSONField(default=list)
    club_recording_url = CharField(null=True)
    club_event_id = IntegerField(index=True, null=True)
    club_event_url = CharField(null=True)
    private_recording_duration_s = IntegerField(null=True)
    public_recording_url = CharField(null=True)
    public_recording_duration_s = IntegerField(null=True)
    view_count = IntegerField(default=0)
    poster_path = CharField(null=True)
    plain_poster_path = CharField(null=True)
    venue = CharField(null=True)
    registration_url = CharField(null=True)

    @property
    def duration_s(self) -> int:
        return max(
            self.public_recording_duration_s or 0,
            self.private_recording_duration_s or 0,
            int((self.end_at - self.start_at).total_seconds()),
        )

    @property
    def has_recording(self) -> bool:
        return bool(self.club_recording_url or self.public_recording_url)

    @property
    def is_public(self) -> bool:
        return bool(self.public_recording_url)

    def get_full_title(self, separator: str = ":") -> str:
        if self.venue:
            return self.title
        return f"{self.bio_name}{separator} {self.title}"

    @property
    def club_recording_message(self) -> ClubMessage | None:
        if not self.club_recording_url:
            return None
        message_id = parse_discord_link(self.club_recording_url)["message_id"]
        return ClubMessage.select().where(ClubMessage.id == message_id).first()

    @property
    def private_recording_url(self) -> str | None:
        if message := self.club_recording_message:
            return get_youtube_url(parse_youtube_id(message.content))
        return None

    @property
    def start_at_prg(self):
        start_at_utc = self.start_at.replace(tzinfo=UTC)
        return start_at_utc.astimezone(ZoneInfo("Europe/Prague")).replace(tzinfo=None)

    @property
    def discord_description(self) -> str:
        return "\n\n".join(
            [
                strip_links(self.short_description or self.description).strip(),
                strip_links(self.bio).strip(),
                self.registration_url if self.registration_url else self.url,
            ]
        )

    @property
    def url(self) -> str:
        return f"https://junior.guru/events/{self.id}/"

    @property
    def page_url(self) -> str:
        return f"events/{self.id}.md"

    def to_card(self) -> dict:
        return dict(
            title=self.title,
            url=self.page_url,
            image_path=self.avatar_path,
            image_alt=self.bio_name,
            subtitle=self.bio_name,
            date=self.start_at,
        )

    def to_json_ld(self) -> str:
        return json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "EducationEvent",
                "educationalLevel": "beginner",
                "endDate": self.end_at.isoformat() + "Z",
                "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
                "image": f"https://junior.guru/static/{self.poster_path}",
                "location": {
                    "@type": "VirtualLocation",
                    "url": (
                        self.public_recording_url
                        or self.club_recording_url
                        or f"https://discord.com/channels/{CLUB_GUILD_ID}/{ClubChannelID.EVENTS}"
                    ),
                },
                "name": self.get_full_title(),
                "startDate": self.start_at.isoformat() + "Z",
                "url": f"https://junior.guru/events/{self.id}/",
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    def to_image_template_context(self, plain: bool = False) -> dict:
        context = {
            "title": self.title,
            "image_path": self.avatar_path,
            "subheading": self.bio_name,
            "date": self.start_at,
        }
        if not plain:
            if self.venue:
                context |= {
                    "button_heading": "Více info na",
                    "button_link": "junior.guru/events",
                }
            else:
                context |= {
                    "button_heading": "Sleduj na",
                    "button_link": (
                        "youtube.com/@juniordotguru"
                        if self.is_public
                        else "junior.guru/events"
                    ),
                    "platforms": (
                        ["discord", "youtube"] if self.is_public else ["discord"]
                    ),
                }
        return context

    def to_thumbnail_meta(self) -> dict:
        meta = {
            f"thumbnail_{key}": value
            for key, value in self.to_image_template_context().items()
        }
        meta["thumbnail_date"] = meta["thumbnail_date"].isoformat()
        return meta

    @classmethod
    def list_speaking_members(cls):
        return (
            ClubUser.select()
            .where(ClubUser.is_member == True)  # noqa: E712
            .join(EventSpeaking)
        )

    @classmethod
    def listing(cls):
        return cls.select().order_by(cls.start_at.desc())

    @classmethod
    def api_listing(cls):
        return cls.listing()

    @classmethod
    def archive_listing(
        cls, now=None, has_recording: bool = False, has_avatar: bool = False
    ):
        now = now or datetime.now(UTC).replace(tzinfo=None)
        query = cls.select().where(cls.start_at < now).order_by(cls.start_at.desc())
        if has_recording:
            query = query.where(
                (cls.club_recording_url.is_null(False))
                | (cls.public_recording_url.is_null(False))  # noqa: E712
            )
        if has_avatar:
            query = query.where(cls.avatar_path != cls.avatar_path.default)
        return query

    @classmethod
    def planned_listing(cls, now=None):
        now = now or datetime.now(UTC).replace(tzinfo=None)
        return cls.select().where(cls.start_at >= now).order_by(cls.start_at)

    @classmethod
    def promo_listing(
        cls, now=None, latest_count=4, public_count=2, rest_count=5
    ) -> list[Self]:
        events = []
        events.extend(
            cls.archive_listing(now=now)
            .where(cls.avatar_path != cls.avatar_path.default)
            .limit(latest_count)
        )
        events.extend(
            cls.archive_listing(now=now, has_recording=True)
            .where(
                cls.avatar_path != cls.avatar_path.default,
                cls.id.not_in([e.id for e in events]),
            )
            .order_by(cls.view_count.desc())
            .limit(public_count)
        )
        events.extend(
            random.sample(
                list(
                    cls.archive_listing(now=now)
                    .where(
                        cls.public_recording_url.is_null(True),
                        cls.avatar_path != cls.avatar_path.default,
                        cls.id.not_in([e.id for e in events]),
                    )
                    .order_by(cls.view_count.desc())
                    .limit(rest_count)
                ),
                k=rest_count,
            )
        )
        return events

    @classmethod
    def count_by_month(cls, date):
        from_date, to_date = month_range(date)
        return (
            cls.select()
            .where(
                fn.date_trunc("day", cls.start_at) >= from_date,
                fn.date_trunc("day", cls.start_at) <= to_date,
            )
            .count()
        )

    @classmethod
    def count_by_month_ttm(cls, date):
        from_date, to_date = ttm_range(date)
        return math.ceil(
            cls.select()
            .where(
                fn.date_trunc("day", cls.start_at) >= from_date,
                fn.date_trunc("day", cls.start_at) <= to_date,
            )
            .count()
            / 12.0
        )


class EventSpeaking(BaseModel):
    speaker = ForeignKeyField(ClubUser, backref="list_speaking")
    event = ForeignKeyField(Event, backref="list_speaking")

    @classmethod
    def listing(cls, from_date, to_date):
        return (
            cls.select()
            .join(Event)
            .where(
                fn.date_trunc("day", Event.start_at) >= from_date,
                fn.date_trunc("day", Event.start_at) <= to_date,
            )
        )

    @classmethod
    def count_ttm(cls, date):
        return math.ceil(cls.listing(*ttm_range(date)).count())

    @classmethod
    def women_listing(cls, from_date, to_date):
        return (
            cls.listing(from_date, to_date)
            .switch(cls)
            .join(ClubUser)
            .where(ClubUser.has_feminine_name == True)  # noqa: E712
        )

    @classmethod
    def women_count_ttm(cls, date):
        return math.ceil(cls.women_listing(*ttm_range(date)).count())

    @classmethod
    def women_ptc_ttm(cls, date):
        count = cls.count_ttm(date)
        if count:
            return math.ceil((cls.women_count_ttm(date) / count) * 100)
        return 0
