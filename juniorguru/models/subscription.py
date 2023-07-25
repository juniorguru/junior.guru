from collections import Counter
from datetime import date
from enum import StrEnum, unique
from functools import wraps
from numbers import Number
from typing import Callable, Iterable, Self

from peewee import BooleanField, CharField, DateField, DateTimeField, fn, Case
from juniorguru.lib.charts import month_range

from juniorguru.models.base import BaseModel, check_enum


LEGACY_PLANS_DELETED_ON = date(2023, 2, 24)


@unique
class SubscriptionActivityType(StrEnum):
    TRIAL_START = 'trial_start'
    TRIAL_END = 'trial_end'
    ORDER = 'order'
    DEACTIVATION = 'deactivation'


@unique
class SubscriptionInterval(StrEnum):
    MONTH = 'month'
    YEAR = 'year'


@unique
class SubscriptionType(StrEnum):
    FREE = 'free'
    FINAID = 'finaid'
    INDIVIDUAL = 'individual'
    TRIAL = 'trial'
    PARTNER = 'partner'
    STUDENT = 'student'


def uses_data_from_subscriptions(default: Callable=None) -> Callable:
    def decorator(class_method: Callable) -> Callable:
        @wraps(class_method)
        def wrapper(cls, date) -> None | Number:
            if is_missing_subscriptions_data(date):
                return default() if default is not None else None
            return class_method(cls, date)
        return wrapper
    return decorator


def is_missing_subscriptions_data(month: date) -> bool:
    if month < LEGACY_PLANS_DELETED_ON:
        return True
    if month_range(month) == month_range(LEGACY_PLANS_DELETED_ON):
        return True
    return False


class SubscriptionActivity(BaseModel):
    class Meta:
        indexes = (
            (('type', 'account_id', 'happened_on'), True),
        )

    type = CharField(constraints=[check_enum('type', SubscriptionActivityType)])
    account_id = CharField(index=True)
    account_has_feminine_name = BooleanField()
    happened_on = DateField()
    happened_at = DateTimeField(index=True)
    order_coupon = CharField(null=True)
    subscription_interval = CharField(null=True, constraints=[check_enum('subscription_interval', SubscriptionInterval)])
    subscription_type = CharField(null=True, constraints=[check_enum('subscription_type', SubscriptionType)])

    @classmethod
    def add(cls, **kwargs):
        unique_key_fields = cls._meta.indexes[0][0]
        conflict_target = [getattr(cls, field) for field in unique_key_fields]
        update = {field: kwargs[field]
                  for field, value in kwargs.items()
                  if ((value is not None) and
                      (field not in unique_key_fields))}
        update[cls.happened_at] = Case(None,
                                       [(cls.happened_at < kwargs['happened_at'], kwargs['happened_at'])],
                                       cls.happened_at)
        insert = cls.insert(**kwargs) \
            .on_conflict(action='update',
                         update=update,
                         conflict_target=conflict_target)
        insert.execute()

    @classmethod
    def total_count(cls) -> int:
        return cls.select().count()

    @classmethod
    def latest_active_listing(cls, date: date) -> Iterable[Self]:
        return cls.select(cls, fn.max(cls.happened_at).alias('latest_at')) \
            .where(cls.happened_on <= date) \
            .group_by(cls.account_id) \
            .having(cls.type != SubscriptionActivityType.DEACTIVATION)

    @classmethod
    def count(cls, date: date) -> int:
        return cls.latest_active_listing(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_count(cls, date: date) -> int | None:
        return cls.latest_active_listing(date) \
            .having(cls.subscription_type == SubscriptionType.INDIVIDUAL) \
            .count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_yearly_count(cls, date: date) -> int | None:
        return cls.latest_active_listing(date) \
            .having(cls.subscription_type == SubscriptionType.INDIVIDUAL,
                    cls.subscription_interval == SubscriptionInterval.YEAR) \
            .count()

    @classmethod
    @uses_data_from_subscriptions(default=dict)
    def count_breakdown(cls, date: date) -> dict[str, int]:
        counter = Counter([activity.subscription_type
                           for activity
                           in cls.latest_active_listing(date)])
        if None in counter:
            raise ValueError("There are members whose latest activity is without subscription type, "
                             f"which can happen only if they're from before {LEGACY_PLANS_DELETED_ON}. "
                             "But then they should be filtered out by the clause HAVING type != deactivation. "
                             "It's very likely these members are deactivated, but it's not reflected in the data. "
                             "See if we shouldn't observe more activities in the ACTIVITY_TYPES_MAPPING.")
        return {subscription_type.value: counter[subscription_type]
                for subscription_type in SubscriptionType}


class SubscriptionCancellation(BaseModel):
    name = CharField()
    email = CharField()
    expires_on = DateField(null=True)
    reason = CharField()
    feedback = CharField(null=True)


class SubscriptionReferrer(BaseModel):
    account_id = CharField()
    name = CharField()
    email = CharField()
    created_on = DateField()
    value = CharField()
    type = CharField(index=True)
    is_internal = BooleanField(index=True)


class SubscriptionMarketingSurvey(BaseModel):
    account_id = CharField()
    name = CharField()
    email = CharField()
    created_on = DateField()
    value = CharField()
    type = CharField(index=True)


# class SubscribedPeriod(BaseModel):
#     account_id = CharField(index=True)
#     start_on = DateField()
#     end_on = DateField()
#     interval_unit = CharField(constraints=[check_enum('interval_unit', SubscribedPeriodIntervalUnit)])
#     type = CharField(null=True, constraints=[check_enum('type', SubscribedPeriodType)])
#     has_feminine_name = BooleanField()

#     @classmethod
#     def listing(cls, date):
#         return cls.select(cls, fn.max(cls.start_on)) \
#             .where(cls.start_on <= date, cls.end_on >= date) \
#             .group_by(cls.account_id) \
#             .order_by(cls.start_on)

#     @classmethod
#     def count(cls, date):
#         return cls.listing(date).count()

#     @classmethod
#     def count_breakdown(cls, date):
#         counter = Counter([subscribed_period.type
#                            for subscribed_period
#                            in cls.listing(date)])
#         return {type.value: counter[type] for type
#                 in SubscribedPeriodType}

#     @classmethod
#     def women_count(cls, date):
#         return cls.listing(date) \
#             .where(cls.has_feminine_name == True) \
#             .count()

#     @classmethod
#     def women_ptc(cls, date):
#         count = cls.count(date)
#         if count:
#             return math.ceil((cls.women_count(date) / count) * 100)
#         return 0

#     @classmethod
#     def individuals(cls, date):
#         return cls.listing(date) \
#             .where(cls.type == SubscribedPeriodType.INDIVIDUALS)

#     @classmethod
#     def individuals_count(cls, date):
#         return cls.individuals(date).count()

#     @classmethod
#     def individuals_yearly_count(cls, date):
#         return cls.individuals(date) \
#             .where(cls.interval_unit == SubscribedPeriodIntervalUnit.YEARLY) \
#             .count()

#     @classmethod
#     def signups(cls, date):
#         from_date, to_date = month_range(date)
#         return cls.select(cls, fn.min(cls.start_on)) \
#             .group_by(cls.account_id) \
#             .having(cls.start_on >= from_date, cls.start_on <= to_date) \
#             .order_by(cls.start_on)

#     @classmethod
#     def signups_count(cls, date):
#         return cls.signups(date).count()

#     @classmethod
#     def individuals_signups(cls, date):
#         return cls.signups(date).where(cls.type == SubscribedPeriodType.INDIVIDUALS)

#     @classmethod
#     def individuals_signups_count(cls, date):
#         return cls.individuals_signups(date).count()

#     @classmethod
#     def quits(cls, date):
#         from_date, to_date = month_range(date)
#         return cls.select(cls, fn.max(cls.end_on)) \
#             .group_by(cls.account_id) \
#             .having(cls.end_on >= from_date, cls.end_on <= to_date) \
#             .order_by(cls.end_on)

#     @classmethod
#     def quits_count(cls, date):
#         return cls.quits(date).count()

#     @classmethod
#     def individuals_quits(cls, date):
#         return cls.quits(date).where(cls.type == SubscribedPeriodType.INDIVIDUALS)

#     @classmethod
#     def individuals_quits_count(cls, date):
#         return cls.individuals_quits(date).count()

#     @classmethod
#     def churn_ptc(cls, date):
#         from_date = month_range(date)[0]
#         churn = cls.quits_count(date) / (cls.count(from_date) + cls.signups_count(date))
#         return churn * 100

#     @classmethod
#     def individuals_churn_ptc(cls, date):
#         from_date = month_range(date)[0]
#         churn = cls.individuals_quits_count(date) / (cls.individuals_count(from_date) + cls.individuals_signups_count(date))
#         return churn * 100

#     @classmethod
#     def individuals_duration_avg(cls, date):
#         from_date, to_date = month_range(date)
#         results = cls.select(cls.account_id, fn.min(cls.start_on), fn.max(cls.end_on)) \
#             .where(cls.type == SubscribedPeriodType.INDIVIDUALS) \
#             .group_by(cls.account_id) \
#             .having(fn.min(cls.start_on) <= from_date)
#         if not results:
#             return 0
#         durations = [((min(to_date, result.end_on) - result.start_on).days / 30) for result in results]
#         return sum(durations) / len(durations)
