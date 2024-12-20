import math
from datetime import date, datetime, time
from typing import Iterable, Self
from zoneinfo import ZoneInfo

from peewee import BooleanField, CharField, DateField, IntegerField

from jg.coop.lib.charts import ttm_range
from jg.coop.models.base import BaseModel


class PodcastEpisode(BaseModel):
    number = IntegerField(primary_key=True)
    publish_on = DateField(unique=True)
    title = CharField()
    guest_name = CharField(null=True)
    guest_has_feminine_name = BooleanField(null=True)
    guest_affiliation = CharField(null=True)
    image_path = CharField()
    media_slug = CharField(unique=True)
    media_url = CharField()
    media_size = IntegerField()
    media_type = CharField()
    media_duration_s = IntegerField()
    description = CharField()
    poster_path = CharField(null=True)

    @property
    def global_id(self) -> str:
        return f"podcast.junior.guru#{self.media_slug}"

    def format_title(self, number: bool = False, affiliation: bool = True) -> str:
        title = ""
        if number:
            title += f"#{self.number} "
        if self.guest_name:
            title += self.guest_name
            if affiliation and self.guest_affiliation:
                title += f" ({self.guest_affiliation})"
            title += " "
        return title + self.title

    @property
    def url(self) -> str:
        return f"https://junior.guru/podcast/{self.number}/"

    @property
    def page_url(self) -> str:
        return f"podcast/{self.number}.jinja"

    @property
    def publish_at_prg(self) -> datetime:
        return datetime.combine(
            self.publish_on,
            time(hour=1, minute=42, second=42),
            tzinfo=ZoneInfo("Europe/Prague"),
        )

    @property
    def media_duration_m(self):
        return math.ceil(self.media_duration_s / 60)

    def to_card(self) -> dict:
        return dict(
            title=self.format_title(number=False, affiliation=False),
            url=self.page_url,
            image_path=self.image_path,
            image_alt=self.format_title(),
            subtitle=self.guest_affiliation,
            date=self.publish_on,
        )

    @classmethod
    def get_by_number(cls, number: int):
        return cls.get_by_id(number)

    @classmethod
    def last(cls, today=None):
        return cls.listing(today=today).get()

    @classmethod
    def listing(cls, today=None) -> Iterable[Self]:
        today = today or date.today()
        return (
            cls.select().where(cls.publish_on <= today).order_by(cls.publish_on.desc())
        )

    @classmethod
    def api_listing(cls, today=None):
        today = today or date.today()
        return cls.select().where(cls.publish_on <= today).order_by(cls.publish_on)

    @classmethod
    def copyright_year(cls, today=None):
        today = today or date.today()
        last_episode = cls.select().order_by(cls.publish_on.desc()).first()
        if last_episode:
            return last_episode.publish_on.year
        return today.year

    @classmethod
    def guests_listing(cls, from_date, to_date):
        return cls.select().where(
            cls.publish_on >= from_date,
            cls.publish_on <= to_date,
            cls.guest_name.is_null(False),
        )

    @classmethod
    def guests_count_ttm(cls, date):
        return math.ceil(cls.guests_listing(*ttm_range(date)).count())

    @classmethod
    def women_listing(cls, from_date, to_date):
        return cls.guests_listing(from_date, to_date).where(
            cls.guest_has_feminine_name == True  # noqa: E712
        )

    @classmethod
    def women_count_ttm(cls, date):
        return math.ceil(cls.women_listing(*ttm_range(date)).count())

    @classmethod
    def women_ptc_ttm(cls, date):
        count = cls.guests_count_ttm(date)
        if count:
            return math.ceil((cls.women_count_ttm(date) / count) * 100)
        return 0
