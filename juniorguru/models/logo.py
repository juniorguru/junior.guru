import re
from urllib.parse import urlparse
from datetime import date

from peewee import CharField, DateField, IntegerField, ForeignKeyField

from juniorguru.models.base import BaseModel
from juniorguru.models import Metric


class Logo(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    filename = CharField()
    email = CharField()
    link = CharField()
    link_re = CharField()
    months = IntegerField()
    starts_at = DateField()
    expires_at = DateField()

    class AmbiguousMatch(Exception):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.link_re:
            self.link_re = re.escape(urlparse(self.link).netloc)

    @classmethod
    def get_by_url(cls, url):
        logos = []
        for logo in cls.listing():
            if re.search(logo.link_re, url, re.IGNORECASE):
                logos.append(logo)
        if len(logos) < 1:
            raise cls.DoesNotExist(url)
        if len(logos) > 1:
            raise cls.AmbiguousMatch(', '.join([logo.link_re for logo in logos]))
        return logos[0]

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.starts_at <= today, cls.expires_at >= today) \
            .order_by(cls.months.desc(), cls.starts_at)

    @property
    def metrics(self):
        return {}


class LogoMetric(BaseModel):
    logo = ForeignKeyField(Logo, backref='list_metrics')
    name = CharField()
    value = IntegerField()

    @classmethod
    def from_values_per_date(cls, logo, name, values):
        return cls(logo=logo, name=name, value=sum(
            value for date, value in values.items()
            if date >= logo.starts_at and date <= logo.expires_at
        ))
