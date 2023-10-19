import math
from datetime import datetime, timedelta

import arrow
from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    TextField,
    fn,
)

from juniorguru.lib.charts import month_range, ttm_range
from juniorguru.lib.md import strip_links
from juniorguru.models.base import BaseModel, JSONField
from juniorguru.models.club import ClubUser
from juniorguru.models.partner import Partner


class Event(BaseModel):
    title = CharField()
    start_at = DateTimeField(index=True)
    description = TextField()
    short_description = TextField(null=True)
    bio = TextField()
    avatar_path = CharField(default='icon.svg')
    bio_name = TextField()
    bio_title = TextField(null=True)
    bio_links = JSONField(default=list)
    partner = ForeignKeyField(Partner, backref='list_events', null=True)
    recording_url = CharField(null=True)
    public_recording_url = CharField(null=True)
    poster_yt_path = CharField(null=True)
    poster_dc_path = CharField(null=True)
    logo_path = CharField(null=True)
    discord_id = IntegerField(index=True, null=True)
    discord_url = CharField(null=True)

    @property
    def full_title(self) -> str:
        return f"{self.bio_name} – {self.title}"

    @property
    def start_at_prg(self):
        return arrow.get(self.start_at).to('Europe/Prague').naive

    @property
    def end_at(self):
        return self.start_at + timedelta(hours=1)

    @property
    def discord_description(self) -> str:
        return '\n\n'.join([
            strip_links(self.description).strip(),
            strip_links(self.bio).strip(),
            self.url,
        ])

    @property
    def url(self):
        return f"https://junior.guru/events/{self.id}/"

    @property
    def page_url(self) -> str:
        return f'events/{self.id}.md'

    def to_card(self) -> dict:
        return dict(
            title=self.title,
            url=self.page_url,
            image_path=self.avatar_path,
            image_alt=self.bio_name,
            subtitle=self.bio_name,
            date=self.start_at,
        )

    @classmethod
    def next(cls, now=None):
        now = now or datetime.utcnow()
        return cls.select() \
            .where(cls.start_at >= now) \
            .order_by(cls.start_at) \
            .first()

    @classmethod
    def list_speaking_members(cls):
        return ClubUser.select() \
            .where(ClubUser.is_member == True) \
            .join(EventSpeaking)

    @classmethod
    def listing(cls):
        return cls.select() \
            .order_by(cls.start_at.desc())

    @classmethod
    def api_listing(cls):
        return cls.listing()

    @classmethod
    def archive_listing(cls, now=None):
        now = now or datetime.utcnow()
        return cls.select() \
            .where(cls.start_at < now) \
            .order_by(cls.start_at.desc())

    @classmethod
    def planned_listing(cls, now=None):
        now = now or datetime.utcnow()
        return cls.select() \
            .where(cls.start_at >= now) \
            .order_by(cls.start_at)

    @classmethod
    def promo_listing(cls, now=None):
        return cls.archive_listing(now=now) \
            .where(cls.avatar_path != cls.avatar_path.default)

    @classmethod
    def count_by_month(cls, date):
        from_date, to_date = month_range(date)
        return cls.select() \
            .where(fn.date_trunc('day', cls.start_at) >= from_date,
                   fn.date_trunc('day', cls.start_at) <= to_date) \
            .count()

    @classmethod
    def count_by_month_ttm(cls, date):
        from_date, to_date = ttm_range(date)
        return math.ceil(cls.select() \
            .where(fn.date_trunc('day', cls.start_at) >= from_date,
                   fn.date_trunc('day', cls.start_at) <= to_date) \
            .count() / 12.0)


class EventSpeaking(BaseModel):
    speaker = ForeignKeyField(ClubUser, backref='list_speaking')
    event = ForeignKeyField(Event, backref='list_speaking')

    @classmethod
    def listing(cls, from_date, to_date):
        return cls.select() \
            .join(Event) \
            .where(fn.date_trunc('day', Event.start_at) >= from_date,
                   fn.date_trunc('day', Event.start_at) <= to_date)

    @classmethod
    def count_ttm(cls, date):
        return math.ceil(cls.listing(*ttm_range(date)).count())

    @classmethod
    def women_listing(cls, from_date, to_date):
        return cls.listing(from_date, to_date) \
            .switch(cls) \
            .join(ClubUser) \
            .where(ClubUser.has_feminine_name == True)

    @classmethod
    def women_count_ttm(cls, date):
        return math.ceil(cls.women_listing(*ttm_range(date)).count())

    @classmethod
    def women_ptc_ttm(cls, date):
        count = cls.count_ttm(date)
        if count:
            return math.ceil((cls.women_count_ttm(date) / count) * 100)
        return 0
