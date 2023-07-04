import math
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from peewee import CharField, DateField, ForeignKeyField, IntegerField, BooleanField
from juniorguru.lib.charts import ttm_range

from juniorguru.models.base import BaseModel
from juniorguru.models.partner import Partner


class PodcastEpisode(BaseModel):
    id = CharField(primary_key=True)
    publish_on = DateField(unique=True)
    title = CharField()
    participant_name = CharField(null=True)
    participant_has_feminine_name = BooleanField(null=True)
    companies = CharField(null=True)
    media_url = CharField()
    media_size = IntegerField()
    media_type = CharField()
    media_duration_s = IntegerField()
    description = CharField()
    partner = ForeignKeyField(Partner, backref='list_podcast_episodes', null=True)
    avatar_path = CharField()
    poster_path = CharField(null=True)

    @property
    def global_id(self):
        return f'podcast.junior.guru#{self.id}'

    @property
    def number(self):
        return int(self.id)

    @property
    def title_numbered(self):
        return f"#{self.number} {self.title}"

    @property
    def slug(self):
        return f'episode{self.id}'

    @property
    def url(self):
        return f'https://junior.guru/podcast/#{self.slug}'

    @property
    def publish_at_prg(self):
        return datetime.combine(self.publish_on,
                                time(hour=1, minute=42, second=42),
                                tzinfo=ZoneInfo('Europe/Prague'))

    @property
    def media_duration_m(self):
        return math.ceil(self.media_duration_s / 60)

    @classmethod
    def last(cls, today=None):
        return cls.listing(today=today).get()

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.publish_on <= today) \
            .order_by(cls.publish_on.desc())

    @classmethod
    def api_listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.publish_on <= today) \
            .order_by(cls.publish_on)

    @classmethod
    def copyright_year(cls, today=None):
        today = today or date.today()
        last_episode = cls.select() \
            .order_by(cls.publish_on.desc()) \
            .first()
        if last_episode:
            return last_episode.publish_on.year
        return today.year

    @classmethod
    def guests_listing(cls, from_date, to_date):
        return cls.select() \
            .where(cls.publish_on >= from_date,
                   cls.publish_on <= to_date,
                   cls.participant_name.is_null(False))

    @classmethod
    def guests_count_ttm(cls, date):
        return math.ceil(cls.guests_listing(*ttm_range(date)).count())

    @classmethod
    def women_listing(cls, from_date, to_date):
        return cls.guests_listing(from_date, to_date) \
            .where(cls.participant_has_feminine_name == True)

    @classmethod
    def women_count_ttm(cls, date):
        return math.ceil(cls.women_listing(*ttm_range(date)).count())

    @classmethod
    def women_ptc_ttm(cls, date):
        count = cls.guests_count_ttm(date)
        if count:
            return math.ceil((cls.women_count_ttm(date) / count) * 100)
        return 0
