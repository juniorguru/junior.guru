import math
from collections.abc import Iterable
from datetime import date, datetime, time
from typing import Self
from zoneinfo import ZoneInfo

from peewee import BooleanField, CharField, DateField, IntegerField

from jg.coop.lib import json_ld
from jg.coop.lib.charts import ttm_range
from jg.coop.lib.social import YOUTUBE_URL
from jg.coop.models.base import BaseModel


PODCAST_NAME = "Junior Guru: programování a kariéra v IT"

PODCAST_URL = "https://junior.guru/podcast/"

PODCAST_ID = f"{PODCAST_URL}#series"

PODCAST_FEED_URL = "https://junior.guru/api/podcast.xml"

PODCAST_IMAGE_URL = "https://junior.guru/static/podcast-v1.png"

PODCAST_YOUTUBE_URL = YOUTUBE_URL

PODCAST_SPOTIFY_URL = "https://open.spotify.com/show/12w93IKRzfCsgo7XrGEVw4"

PODCAST_APPLE_URL = (
    "https://podcasts.apple.com/cz/podcast/junior-guru-podcast/id1603653549"
)


def podcast_series_json_ld() -> str:
    return json_ld.dumps(
        {
            "@type": "PodcastSeries",
            "@id": PODCAST_ID,
            "name": PODCAST_NAME,
            "url": PODCAST_URL,
            "inLanguage": "cs",
            "webFeed": PODCAST_FEED_URL,
            "image": PODCAST_IMAGE_URL,
            "sameAs": [PODCAST_YOUTUBE_URL, PODCAST_SPOTIFY_URL, PODCAST_APPLE_URL],
        }
    )


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
    def page_description(self) -> str:
        intro = f"V {self.number}. dílu Junior Guru podcastu"
        if not self.guest_name:
            return f"{intro}: {self.title}"
        if " a " in self.guest_name:
            guest = "jsou hosty"
        elif self.guest_has_feminine_name:
            guest = "je hostkou"
        else:
            guest = "je hostem"
        if self.guest_affiliation:
            return f"{intro} {guest} {self.guest_name} ({self.guest_affiliation})."
        return f"{intro} {guest} {self.guest_name}."

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
        return {
            "title": self.format_title(number=False, affiliation=False),
            "url": self.page_url,
            "image_path": self.image_path,
            "image_alt": self.format_title(),
            "subtitle": self.guest_affiliation,
            "date": self.publish_on,
        }

    def to_json_ld(self) -> str:
        return json_ld.dumps(
            {
                "@type": "PodcastEpisode",
                "associatedMedia": {
                    "@type": "MediaObject",
                    "contentSize": str(self.media_size),
                    "contentUrl": self.media_url,
                    "encodingFormat": self.media_type,
                },
                "datePublished": self.publish_on.isoformat(),
                "description": self.description,
                "duration": f"PT{self.media_duration_s}S",
                "episodeNumber": self.number,
                "image": f"https://junior.guru/static/{self.image_path}",
                "inLanguage": "cs",
                "name": self.format_title(),
                "partOfSeries": {
                    "@type": "PodcastSeries",
                    "@id": PODCAST_ID,
                    "name": PODCAST_NAME,
                    "url": PODCAST_URL,
                },
                "url": self.url,
            }
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
            cls.guest_has_feminine_name == True
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
