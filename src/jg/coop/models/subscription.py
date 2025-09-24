from collections import Counter
from datetime import date, timedelta
from enum import StrEnum, unique
from typing import Iterable, Self

from peewee import (
    Case,
    CharField,
    DateField,
    IntegerField,
    fn,
)

from jg.coop.lib.charts import month_range
from jg.coop.models.base import BaseModel, check_enum
from jg.coop.models.club import ClubUser


@unique
class SubscriptionInterval(StrEnum):
    MONTH = "month"
    YEAR = "year"


@unique
class SubscriptionType(StrEnum):
    FREE = "free"
    FINAID = "finaid"
    INDIVIDUAL = "individual"
    TRIAL = "trial"
    SPONSOR = "sponsor"


@unique
class SubscriptionCancellationReason(StrEnum):
    OTHER = "other"
    NECESSITY = "necessity"
    AFFORDABILITY = "affordability"
    TEMPORARY_USE = "temporary_use"
    MISUNDERSTOOD = "misunderstood"
    COMPETITION = "competition"
    UNKNOWN = "unknown"


@unique
class SubscriptionMarketingSurveyAnswer(StrEnum):
    YABLKO = "yablko"
    FRIEND = "friend"
    PODCASTS = "podcasts"
    COURSES = "courses"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    COURSES_SEARCH = "courses_search"
    SEARCH = "search"
    INTERNET = "internet"
    OTHER = "other"


@unique
class SubscriptionReferrerType(StrEnum):
    HONZAJAVOREK = "honzajavorek"
    YOUTUBE = "youtube"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    GOOGLE = "google"
    OTHER = "other"


class SubscriptionCancellation(BaseModel):
    account_id = IntegerField(unique=True)
    account_name = CharField()
    account_email = CharField()
    account_total_spend = IntegerField()
    expires_on = DateField(null=True)
    reason = CharField(
        index=True, constraints=[check_enum("reason", SubscriptionCancellationReason)]
    )
    feedback = CharField(null=True)

    @classmethod
    def add(cls, **kwargs) -> None:
        if kwargs["expires_on"] is None:
            cls.insert(**kwargs).on_conflict_ignore().execute()
        else:
            update = {
                field: Case(
                    None,
                    [
                        (cls.expires_on.is_null(True), value),
                        (
                            cls.expires_on.is_null(False)
                            & (cls.expires_on < kwargs["expires_on"]),
                            value,
                        ),
                    ],
                    getattr(cls, field),
                )
                for field, value in kwargs.items()
            }
            cls.insert(**kwargs).on_conflict(
                action="update", update=update, conflict_target=[cls.account_id]
            ).execute()

    @property
    def user(self) -> ClubUser:
        return ClubUser.select().where(ClubUser.account_id == self.account_id).first()

    @classmethod
    def report_listing(cls, exclude_account_ids=None) -> Iterable[Self]:
        exclude_account_ids = exclude_account_ids or []
        return (
            cls.select()
            .where(cls.account_id.not_in(exclude_account_ids))
            .order_by(cls.expires_on)
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def breakdown_ptc(cls, date: date) -> dict[str, float]:
        from_date, to_date = month_range(date)
        query = cls.select().where(
            cls.expires_on >= from_date, cls.expires_on <= to_date
        )
        counter = Counter([cancellation.reason for cancellation in query])
        return get_breakdown_ptc(counter, SubscriptionCancellationReason)

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select()
        counter = Counter([cancellation.reason for cancellation in query])
        return get_breakdown_ptc(counter, SubscriptionCancellationReason)


class SubscriptionReferrer(BaseModel):
    account_id = IntegerField(unique=True)
    account_name = CharField()
    account_email = CharField()
    account_total_spend = IntegerField()
    created_on = DateField()
    url = CharField()
    type = CharField(
        index=True, constraints=[check_enum("type", SubscriptionReferrerType)]
    )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select()
        counter = Counter([referrer.type for referrer in query])
        return get_breakdown_ptc(counter, SubscriptionReferrerType)

    @classmethod
    def total_spend_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select(cls.type, cls.account_total_spend)
        counter = Counter()
        for type, account_total_spend in query.tuples():
            counter[type] += account_total_spend
        return get_breakdown_ptc(counter, SubscriptionReferrerType)


class SubscriptionInternalReferrer(BaseModel):
    account_id = IntegerField(unique=True)
    account_name = CharField()
    account_email = CharField()
    account_total_spend = IntegerField()
    created_on = DateField()
    url = CharField()
    path = CharField(index=True)

    @classmethod
    def count(cls, period_days: int) -> int:
        return (
            cls.select()
            .where(cls.created_on >= cls.latest_on() - timedelta(days=period_days))
            .count()
        )

    @classmethod
    def latest_on(cls) -> date:
        return cls.select(fn.max(cls.created_on)).scalar()

    @classmethod
    def total_breakdown_ptc(
        cls, period_days: int, most_common: int = 20
    ) -> dict[str, float]:
        query = cls.select().where(
            cls.created_on >= cls.latest_on() - timedelta(days=period_days)
        )
        counter = Counter([referrer.path for referrer in query])
        counter = dict(counter.most_common(most_common))
        return get_breakdown_ptc(counter)

    @classmethod
    def total_spend_breakdown_ptc(
        cls, period_days: int, most_common: int = 20
    ) -> dict[str, float]:
        query = cls.select(cls.path, cls.account_total_spend).where(
            cls.created_on >= cls.latest_on() - timedelta(days=period_days)
        )
        counter = Counter()
        for path, account_total_spend in query.tuples():
            counter[path] += account_total_spend
        counter = dict(counter.most_common(most_common))
        return get_breakdown_ptc(counter)


class SubscriptionMarketingSurvey(BaseModel):
    account_id = IntegerField(unique=True)
    account_name = CharField()
    account_email = CharField()
    account_total_spend = IntegerField()
    created_on = DateField()
    value = CharField()
    type = CharField(
        index=True, constraints=[check_enum("type", SubscriptionMarketingSurveyAnswer)]
    )

    @property
    def user(self) -> ClubUser:
        return ClubUser.select().where(ClubUser.account_id == self.account_id).first()

    @classmethod
    def report_listing(cls, exclude_account_ids=None) -> Iterable[Self]:
        exclude_account_ids = exclude_account_ids or []
        return (
            cls.select()
            .where(cls.account_id.not_in(exclude_account_ids))
            .order_by(cls.created_on)
        )

    @classmethod
    def count(cls) -> int:
        return cls.select().count()

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select()
        counter = Counter([answer.type for answer in query])
        return get_breakdown_ptc(counter, SubscriptionMarketingSurveyAnswer)

    @classmethod
    def total_spend_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select(cls.type, cls.account_total_spend)
        counter = Counter()
        for type, account_total_spend in query.tuples():
            counter[type] += account_total_spend
        return get_breakdown_ptc(counter, SubscriptionMarketingSurveyAnswer)


class SubscriptionCountry(BaseModel):
    customer_id = CharField(unique=True)
    country_code = CharField()

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select().order_by(cls.country_code)
        counter = Counter(
            [
                (
                    country.country_code
                    if country.country_code in ["CZ", "SK"]
                    else "other"
                )
                for country in query
            ]
        )
        return get_breakdown_ptc(counter)


def get_breakdown_ptc(counter: dict, enum: StrEnum | None = None) -> dict[str, float]:
    if enum is None:
        types = list(counter.keys())
    else:
        types = [type.value for type in enum]
    if total_count := sum(counter.values()):
        return {type: (counter[type] / total_count) * 100 for type in types}
    return {type: 0 for type in types}
