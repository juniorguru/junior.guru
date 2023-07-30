import json
import math
from collections import Counter
from datetime import date, datetime, timedelta
from enum import StrEnum, unique
from functools import wraps
from numbers import Number
from typing import Callable, Generator, Iterable, Self

from peewee import (BooleanField, Case, CharField, DateField, DateTimeField,
                    IntegerField, fn)
from playhouse.shortcuts import model_to_dict

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


@unique
class SubscriptionCancellationReason(StrEnum):
    OTHER = 'other'
    NECESSITY = 'necessity'
    AFFORDABILITY = 'affordability'
    TEMPORARY_USE = 'temporary_use'
    MISUNDERSTOOD = 'misunderstood'
    COMPETITION = 'competition'


@unique
class SubscriptionMarketingSurveyAnswer(StrEnum):
    YABLKO = 'yablko'
    PODCASTS = 'podcasts'
    COURSES_SEARCH = 'courses_search'
    COURSES = 'courses'
    YOUTUBE = 'youtube'
    FACEBOOK = 'facebook'
    LINKEDIN = 'linkedin'
    SEARCH = 'search'
    FRIEND = 'friend'
    OTHER = 'other'


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
    account_id = IntegerField(index=True)
    account_has_feminine_name = BooleanField()
    happened_on = DateField(index=True)
    happened_at = DateTimeField(index=True)
    order_coupon_slug = CharField(null=True)
    subscription_interval = CharField(null=True, constraints=[check_enum('subscription_interval', SubscriptionInterval)])
    subscription_type = CharField(null=True, constraints=[check_enum('subscription_type', SubscriptionType)])

    @classmethod
    def deserialize(cls, line: str) -> Self:
        data = json.loads(line)
        data['account_has_feminine_name'] = data.pop('f')
        data['happened_at'] = datetime.fromisoformat(data['happened_at'])
        data['happened_on'] = data['happened_at'].date()
        return cls.add(**data)

    def serialize(self) -> str:
        # most of the following is done to save bytes
        drop_fields = [
            'id',  # irrelevant
            'happened_on',  # can be computed from 'happened_at'
            'subscription_type',  # can be computed from 'order_coupon_slug'
        ]
        data = {field: value for field, value
                in model_to_dict(self).items()
                if value is not None and field not in drop_fields}
        data['f'] = data.pop('account_has_feminine_name')  # saves bytes
        data['happened_at'] = data['happened_at'].isoformat()
        return json.dumps(data, sort_keys=True, ensure_ascii=False) + '\n'

    @classmethod
    def add(cls, **kwargs) -> None:
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
    def history_end_on(cls, buffer_days=30) -> date:
        # The 'trial_end' activities are sometimes in the future,
        # so let's not consider them as the end of the known history
        end_on = cls.select(cls.happened_at) \
            .where(cls.type != SubscriptionActivityType.TRIAL_END) \
            .order_by(cls.happened_at.desc()) \
            .limit(1) \
            .scalar()
        if end_on:
            return end_on - timedelta(days=buffer_days)
        return None

    @classmethod
    def history(cls) -> Iterable[Self]:
        # Saving only everything before the end, to avoid overlaps
        return cls.select() \
            .where(cls.happened_on < cls.history_end_on()) \
            .order_by(cls.happened_at)

    @classmethod
    def cleanse_data(cls) -> None:
        # The 'order' activity happening on the same day as 'trial_end' activity
        # marks subscription type of the whole trial.
        #
        # If the 'order' activity is for an individual subscription, we can assume
        # the trial was a true trial and not something free or paid by invoice. Hence
        # we can mark all the trial activities with a special subscription type 'trial'.
        #
        # If there's no such order, we can also assume the trial was a true trial,
        # albeit not finished yet, or not followed by an order (deactivated).
        trial_ends = cls.select() \
            .where(cls.type == SubscriptionActivityType.TRIAL_END,
                   cls.subscription_type == SubscriptionType.INDIVIDUAL,
                   cls.happened_on > LEGACY_PLANS_DELETED_ON)
        for trial_end in trial_ends:
            account_activities = cls.select().where(cls.account_id == trial_end.account_id)

            new_order = account_activities \
                .where(cls.type == SubscriptionActivityType.ORDER,
                       cls.happened_on == trial_end.happened_on) \
                .first()

            if not new_order or new_order.subscription_type == SubscriptionType.INDIVIDUAL:
                subscription_type = SubscriptionType.TRIAL
            else:
                subscription_type = new_order.subscription_type

            trial_end.subscription_type = subscription_type
            trial_end.save()
            trial_start = account_activities \
                .where(cls.type == SubscriptionActivityType.TRIAL_START,
                       cls.happened_on < trial_end.happened_on) \
                .get()
            trial_start.subscription_type = subscription_type
            trial_start.save()
            trial_order = account_activities \
                .where(cls.type == SubscriptionActivityType.ORDER,
                       cls.happened_on == trial_start.happened_on) \
                .first()
            trial_order.subscription_type = subscription_type
            trial_order.save()

        # By default 'deactivation' activities are without details, so let's
        # give it the details of the latest activity before it.
        deactivations = cls.select() \
            .where(cls.type == SubscriptionActivityType.DEACTIVATION,
                   cls.happened_on > LEGACY_PLANS_DELETED_ON)
        for deactivation in deactivations:
            previous_activity = cls.select() \
                .where(cls.type != SubscriptionActivityType.DEACTIVATION,
                       cls.account_id == deactivation.account_id,
                       cls.happened_at <= deactivation.happened_at) \
                .order_by(cls.happened_at.desc()) \
                .get()
            deactivation.subscription_type = previous_activity.subscription_type
            deactivation.subscription_interval = previous_activity.subscription_interval
            deactivation.save()

    @classmethod
    def total_count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls, date: date) -> Iterable[Self]:
        latest_at = fn.max(cls.happened_at).alias('latest_at')
        latest = cls.select(cls.account_id, latest_at) \
            .where(cls.happened_on <= date) \
            .group_by(cls.account_id)
        return cls.select(cls) \
            .join(latest, on=((cls.account_id == latest.c.account_id) &
                              (cls.happened_at == latest.c.latest_at)))

    @classmethod
    def active_listing(cls, date: date) -> Iterable[Self]:
        return cls.listing(date) \
            .where(cls.type != SubscriptionActivityType.DEACTIVATION)

    @classmethod
    def active_count(cls, date: date) -> int:
        return cls.active_listing(date).count()

    @classmethod
    def active_individuals_listing(cls, date: date) -> Iterable[Self]:
        return cls.active_listing(date) \
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL)

    @classmethod
    @uses_data_from_subscriptions()
    def active_individuals_count(cls, date: date) -> int | None:
        return cls.active_individuals_listing(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def active_individuals_yearly_count(cls, date: date) -> int | None:
        return cls.active_listing(date) \
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL,
                   cls.subscription_interval == SubscriptionInterval.YEAR) \
            .count()

    @classmethod
    @uses_data_from_subscriptions(default=dict)
    def active_subscription_type_breakdown(cls, date: date) -> dict[str, int]:
        counter = Counter([activity.subscription_type for activity in cls.active_listing(date)])
        if None in counter:
            raise ValueError("There are members whose latest activity is without subscription type, "
                             f"which can happen only if they're from before {LEGACY_PLANS_DELETED_ON}. "
                             "But then they should be filtered out by the clause HAVING type != deactivation. "
                             "It's very likely these members are deactivated, but it's not reflected in the data. "
                             "See if we shouldn't observe more activities in the ACTIVITY_TYPES_MAPPING.")
        return {subscription_type.value: counter[subscription_type]
                for subscription_type in SubscriptionType}

    @classmethod
    def active_women_count(cls, date: date) -> int:
        return cls.active_listing(date) \
            .where(cls.account_has_feminine_name == True) \
            .count()

    @classmethod
    def active_women_ptc(cls, date: date) -> int:
        if count := cls.active_count(date):
            return math.ceil((cls.active_women_count(date) / count) * 100)
        return 0

    @classmethod
    def signups(cls, date: date) -> Iterable[Self]:
        from_date, to_date = month_range(date)
        return cls.select(fn.min(cls.happened_at)) \
            .where(cls.happened_on <= to_date) \
            .group_by(cls.account_id) \
            .having(cls.happened_on >= from_date)

    @classmethod
    def signups_count(cls, date: date) -> int:
        return cls.signups(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_signups_count(cls, date: date) -> int:
        return cls.signups(date) \
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL) \
            .count()

    @classmethod
    def quits(cls, date: date) -> Iterable[Self]:
        from_date, to_date = month_range(date)

        o_cls = cls.alias('orders')
        d_cls = cls.alias('deactivations')

        # Subquery to select when the latest order for given account_id happened
        latest_order_at = o_cls.select(fn.max(o_cls.happened_at)) \
            .where(o_cls.type != SubscriptionActivityType.DEACTIVATION,
                   o_cls.account_id == d_cls.account_id,
                   o_cls.happened_on <= to_date) \
            .group_by(o_cls.account_id) \
            .alias('latest_order_at')

        # The row_num column will allow us to filter out duplicit deactivations
        # and must be ordered ascendingly so that the first occurance
        # of deactivation is row number one
        row_num = fn.row_number() \
            .over(partition_by=[d_cls.account_id, d_cls.type],
                  order_by=[d_cls.happened_at]) \
            .alias('row_num')

        # Then selecting deactivations for each account_id which happen
        # later than the latest order, and we keep track of the row number
        deactivations = d_cls.select(d_cls.id, row_num) \
            .where(d_cls.type == SubscriptionActivityType.DEACTIVATION,
                   d_cls.happened_at >= latest_order_at,
                   d_cls.happened_on <= to_date) \
            .order_by(d_cls.account_id, d_cls.happened_at.desc()) \
            .alias('deactivations')

        # Now selecting only the first row for each account_id, effectively
        # getting rid of later duplicit deactivations
        return cls.select(cls) \
            .join(deactivations, on=(cls.id == deactivations.c.id)) \
            .where(deactivations.c.row_num == 1,
                   cls.happened_on >= from_date)

    @classmethod
    def quits_count(cls, date: date) -> int:
        return cls.quits(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_quits_count(cls, date: date) -> int:
        return cls.quits(date) \
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL) \
            .count()

    @classmethod
    def churn_ptc(cls, date):
        from_date = month_range(date)[0]
        churn = cls.quits_count(date) / (cls.active_count(from_date) + cls.signups_count(date))
        return churn * 100

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_churn_ptc(cls, date):
        from_date = month_range(date)[0]
        churn = cls.individuals_quits_count(date) / (cls.active_individuals_count(from_date) + cls.individuals_signups_count(date))
        return churn * 100

    @classmethod
    def active_duration_avg(cls, date: date) -> int:
        account_ids = [activity.account_id for activity in cls.active_listing(date)]
        if durations := list(cls._calc_durations(account_ids, date)):
            return sum(durations) / len(durations)
        return 0

    @classmethod
    @uses_data_from_subscriptions()
    def active_individuals_duration_avg(cls, date: date) -> int:
        account_ids = [activity.account_id for activity in cls.active_individuals_listing(date)]
        if durations := list(cls._calc_durations(account_ids, date)):
            return sum(durations) / len(durations)
        return 0

    @classmethod
    def _calc_durations(cls, account_ids: list[str], date: date) -> Generator[int, None, None]:
        earliest_on = fn.min(cls.happened_on).alias('earliest_on')
        items = cls.select(earliest_on) \
            .where(cls.account_id.in_(account_ids)) \
            .group_by(cls.account_id) \
            .dicts()
        for item in items:
            duration_sec = (date - item['earliest_on']).total_seconds()
            duration_mo = (duration_sec / 60 / 60 / 24 / 30)
            yield duration_mo


class SubscriptionCancellation(BaseModel):
    name = CharField()
    email = CharField()
    expires_on = DateField(null=True)
    reason = CharField(index=True, constraints=[check_enum('reason', SubscriptionCancellationReason)])
    feedback = CharField(null=True)

    @classmethod
    def breakdown_ptc(cls, date: date) -> dict[str, float]:
        from_date, to_date = month_range(date)
        query = cls.select() \
            .where(cls.expires_on >= from_date,
                   cls.expires_on <= to_date)
        counter = Counter([cancellation.reason for cancellation in query])
        total_count = sum(counter.values())
        return {reason.value: (counter[reason] / total_count) * 100
                for reason in SubscriptionCancellationReason}

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select()
        counter = Counter([cancellation.reason for cancellation in query])
        total_count = sum(counter.values())
        return {reason.value: (counter[reason] / total_count) * 100
                for reason in SubscriptionCancellationReason}


class SubscriptionReferrer(BaseModel):
    account_id = IntegerField()
    name = CharField()
    email = CharField()
    created_on = DateField()
    value = CharField()
    type = CharField(index=True)
    is_internal = BooleanField(index=True)


class SubscriptionMarketingSurvey(BaseModel):
    account_id = IntegerField()
    name = CharField()
    email = CharField()
    created_on = DateField()
    value = CharField()
    type = CharField(index=True, constraints=[check_enum('type', SubscriptionMarketingSurveyAnswer)])

    @classmethod
    def breakdown_ptc(cls, date: date) -> dict[str, float]:
        from_date, to_date = month_range(date)
        query = cls.select() \
            .where(cls.created_on >= from_date,
                   cls.created_on <= to_date)
        counter = Counter([answer.type for answer in query])
        total_count = sum(counter.values())
        return {type.value: (counter[type] / total_count) * 100
                for type in SubscriptionMarketingSurveyAnswer}

    @classmethod
    def total_breakdown_ptc(cls) -> dict[str, float]:
        query = cls.select()
        counter = Counter([answer.type for answer in query])
        total_count = sum(counter.values())
        return {type.value: (counter[type] / total_count) * 100
                for type in SubscriptionMarketingSurveyAnswer}
