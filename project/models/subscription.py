import json
import math
from collections import Counter
from datetime import date, datetime, timedelta
from enum import StrEnum, unique
from functools import wraps
from numbers import Number
from typing import Callable, Generator, Iterable, Self

from peewee import (
    BooleanField,
    Case,
    CharField,
    DateField,
    DateTimeField,
    IntegerField,
    fn,
)
from playhouse.shortcuts import model_to_dict

from project.lib.charts import month_range
from project.models.base import BaseModel, check_enum
from project.models.club import ClubUser


LEGACY_PLANS_DELETED_ON = date(2023, 2, 24)


@unique
class SubscriptionActivityType(StrEnum):
    TRIAL_START = "trial_start"
    TRIAL_END = "trial_end"
    ORDER = "order"
    DEACTIVATION = "deactivation"


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
    PARTNER = "partner"


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


def uses_data_from_subscriptions(default: Callable = None) -> Callable:
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
        indexes = ((("type", "account_id", "happened_on"), True),)

    type = CharField(constraints=[check_enum("type", SubscriptionActivityType)])
    account_id = IntegerField(index=True)
    account_has_feminine_name = BooleanField()
    happened_on = DateField(index=True)
    happened_at = DateTimeField(index=True)
    order_coupon_slug = CharField(null=True)
    subscription_interval = CharField(
        null=True,
        constraints=[check_enum("subscription_interval", SubscriptionInterval)],
    )
    subscription_type = CharField(
        null=True, constraints=[check_enum("subscription_type", SubscriptionType)]
    )

    @classmethod
    def deserialize(cls, line: str) -> Self:
        data = json.loads(line)
        data["account_has_feminine_name"] = data.pop("f")
        data["happened_at"] = datetime.fromisoformat(data["happened_at"])
        data["happened_on"] = data["happened_at"].date()
        return cls.add(**data)

    def serialize(self) -> str:
        # most of the following is done to save bytes
        drop_fields = [
            "id",  # irrelevant
            "happened_on",  # can be computed from 'happened_at'
            "subscription_type",  # can be computed from 'order_coupon_slug'
        ]
        data = {
            field: value
            for field, value in model_to_dict(self).items()
            if value is not None and field not in drop_fields
        }
        data["f"] = data.pop("account_has_feminine_name")  # saves bytes
        data["happened_at"] = data["happened_at"].isoformat()
        return json.dumps(data, sort_keys=True, ensure_ascii=False) + "\n"

    @classmethod
    def add(cls, **kwargs) -> None:
        unique_key_fields = cls._meta.indexes[0][0]
        conflict_target = [getattr(cls, field) for field in unique_key_fields]

        update = {
            field: kwargs[field]
            for field, value in kwargs.items()
            if ((value is not None) and (field not in unique_key_fields))
        }
        update[cls.happened_at] = Case(
            None,
            [(cls.happened_at < kwargs["happened_at"], kwargs["happened_at"])],
            cls.happened_at,
        )

        insert = cls.insert(**kwargs).on_conflict(
            action="update", update=update, conflict_target=conflict_target
        )
        insert.execute()

    @classmethod
    def history_end_on(cls, buffer_days=30) -> date:
        # The 'trial_end' and 'deactivation' activities are sometimes in the future,
        # so let's not consider them as the end of the known history
        end_on = (
            cls.select(cls.happened_at)
            .where(
                cls.type.not_in(
                    [
                        SubscriptionActivityType.TRIAL_END,
                        SubscriptionActivityType.DEACTIVATION,
                    ]
                )
            )
            .order_by(cls.happened_at.desc())
            .limit(1)
            .scalar()
        )
        if end_on:
            return end_on - timedelta(days=buffer_days)
        return None

    @classmethod
    def history(cls) -> Iterable[Self]:
        # Saving only everything before the end, to avoid overlaps
        return (
            cls.select()
            .where(cls.happened_on < cls.history_end_on())
            .order_by(cls.happened_at)
        )

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
        trial_ends = cls.select().where(
            cls.type == SubscriptionActivityType.TRIAL_END,
            cls.subscription_type == SubscriptionType.INDIVIDUAL,
            cls.happened_on > LEGACY_PLANS_DELETED_ON,
        )
        for trial_end in trial_ends:
            account_activities = cls.select().where(
                cls.account_id == trial_end.account_id
            )

            new_order = account_activities.where(
                cls.type == SubscriptionActivityType.ORDER,
                cls.happened_on == trial_end.happened_on,
            ).first()

            if (
                not new_order
                or new_order.subscription_type == SubscriptionType.INDIVIDUAL
            ):
                subscription_type = SubscriptionType.TRIAL
            else:
                subscription_type = new_order.subscription_type

            trial_end.subscription_type = subscription_type
            trial_end.save()
            trial_start = account_activities.where(
                cls.type == SubscriptionActivityType.TRIAL_START,
                cls.happened_on < trial_end.happened_on,
            ).get()
            trial_start.subscription_type = subscription_type
            trial_start.save()
            trial_order = account_activities.where(
                cls.type == SubscriptionActivityType.ORDER,
                cls.happened_on == trial_start.happened_on,
            ).first()
            trial_order.subscription_type = subscription_type
            trial_order.save()

        # Some 'deactivation' activities are without details, so let's
        # give it the details of the latest activity before it.
        deactivations = cls.select().where(
            cls.type == SubscriptionActivityType.DEACTIVATION,
            cls.happened_on > LEGACY_PLANS_DELETED_ON,
        )
        for deactivation in deactivations:
            previous_activity = (
                cls.select()
                .where(
                    cls.type != SubscriptionActivityType.DEACTIVATION,
                    cls.account_id == deactivation.account_id,
                    cls.happened_at <= deactivation.happened_at,
                )
                .order_by(cls.happened_at.desc())
                .get()
            )
            deactivation.subscription_type = previous_activity.subscription_type
            deactivation.subscription_interval = previous_activity.subscription_interval
            deactivation.save()

    @classmethod
    def total_count(cls) -> int:
        return cls.select().count()

    @classmethod
    def listing(cls, date: date) -> Iterable[Self]:
        latest_at = fn.max(cls.happened_at).alias("latest_at")
        latest = (
            cls.select(cls.account_id, latest_at)
            .where(cls.happened_on <= date)
            .group_by(cls.account_id)
        )
        return cls.select(cls).join(
            latest,
            on=(
                (cls.account_id == latest.c.account_id)
                & (cls.happened_at == latest.c.latest_at)
            ),
        )

    @classmethod
    def active_listing(cls, date: date) -> Iterable[Self]:
        return cls.listing(date).where(
            cls.type != SubscriptionActivityType.DEACTIVATION
        )

    @classmethod
    def active_count(cls, date: date) -> int:
        return cls.active_listing(date).count()

    @classmethod
    def active_individuals_listing(cls, date: date) -> Iterable[Self]:
        return cls.active_listing(date).where(
            cls.subscription_type == SubscriptionType.INDIVIDUAL
        )

    @classmethod
    @uses_data_from_subscriptions()
    def active_individuals_count(cls, date: date) -> int | None:
        return cls.active_individuals_listing(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def active_individuals_yearly_count(cls, date: date) -> int | None:
        return (
            cls.active_listing(date)
            .where(
                cls.subscription_type == SubscriptionType.INDIVIDUAL,
                cls.subscription_interval == SubscriptionInterval.YEAR,
            )
            .count()
        )

    @classmethod
    @uses_data_from_subscriptions(default=dict)
    def active_subscription_type_breakdown(cls, date: date) -> dict[str, int]:
        counter = Counter(
            [activity.subscription_type for activity in cls.active_listing(date)]
        )
        if None in counter:
            raise ValueError(
                "There are members whose latest activity is without subscription type, "
                f"which can happen only if they're from before {LEGACY_PLANS_DELETED_ON}. "
                "But then they should be filtered out by the clause HAVING type != deactivation. "
                "It's very likely these members are deactivated, but it's not reflected in the data. "
                "See if we shouldn't observe more activities in the ACTIVITY_TYPES_MAPPING."
            )
        return {
            subscription_type.value: counter[subscription_type]
            for subscription_type in SubscriptionType
        }

    @classmethod
    @uses_data_from_subscriptions(default=dict)
    def trial_conversion_ptc(cls, date: date) -> dict[str, int]:
        from_date, to_date = month_range(date)

        trials = (
            cls.select(cls.account_id)
            .where(
                cls.happened_on <= to_date,
                cls.subscription_type == SubscriptionType.TRIAL,
            )
            .group_by(cls.account_id)
            .having(cls.happened_on >= from_date)
        )
        total_count = trials.count()

        subscriptions = (
            cls.select(cls.account_id)
            .where(
                cls.happened_on >= from_date,
                cls.subscription_type == SubscriptionType.INDIVIDUAL,
            )
            .group_by(cls.account_id)
        )
        converting_trials = trials.intersect(subscriptions)
        converting_count = converting_trials.count()
        return (converting_count / total_count) * 100 if total_count else 0

    @classmethod
    def active_women_count(cls, date: date) -> int:
        return (
            cls.active_listing(date)
            .where(cls.account_has_feminine_name == True)  # noqa: E712
            .count()
        )

    @classmethod
    def active_women_ptc(cls, date: date) -> int:
        if count := cls.active_count(date):
            return math.ceil((cls.active_women_count(date) / count) * 100)
        return 0

    @classmethod
    def signups(cls, date: date) -> Iterable[Self]:
        from_date, to_date = month_range(date)
        return (
            cls.select(fn.min(cls.happened_at))
            .where(cls.happened_on <= to_date)
            .group_by(cls.account_id)
            .having(cls.happened_on >= from_date)
        )

    @classmethod
    def signups_count(cls, date: date) -> int:
        return cls.signups(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_signups_count(cls, date: date) -> int:
        return (
            cls.signups(date)
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL)
            .count()
        )

    @classmethod
    def quits(cls, date: date) -> Iterable[Self]:
        from_date, to_date = month_range(date)

        o_cls = cls.alias("orders")
        d_cls = cls.alias("deactivations")

        # Subquery to select when the latest order for given account_id happened
        latest_order_at = (
            o_cls.select(fn.max(o_cls.happened_at))
            .where(
                o_cls.type != SubscriptionActivityType.DEACTIVATION,
                o_cls.account_id == d_cls.account_id,
                o_cls.happened_on <= to_date,
            )
            .group_by(o_cls.account_id)
            .alias("latest_order_at")
        )

        # The row_num column will allow us to filter out duplicate deactivations
        # and must be ordered ascendingly so that the first occurance
        # of deactivation is row number one
        row_num = (
            fn.row_number()
            .over(
                partition_by=[d_cls.account_id, d_cls.type],
                order_by=[d_cls.happened_at],
            )
            .alias("row_num")
        )

        # Then selecting deactivations for each account_id which happen
        # later than the latest order, and we keep track of the row number
        deactivations = (
            d_cls.select(d_cls.id, row_num)
            .where(
                d_cls.type == SubscriptionActivityType.DEACTIVATION,
                d_cls.happened_at >= latest_order_at,
                d_cls.happened_on <= to_date,
            )
            .order_by(d_cls.account_id, d_cls.happened_at.desc())
            .alias("deactivations")
        )

        # Now selecting only the first row for each account_id, effectively
        # getting rid of later duplicate deactivations
        return (
            cls.select(cls)
            .join(deactivations, on=(cls.id == deactivations.c.id))
            .where(deactivations.c.row_num == 1, cls.happened_on >= from_date)
        )

    @classmethod
    def quits_count(cls, date: date) -> int:
        return cls.quits(date).count()

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_quits_count(cls, date: date) -> int:
        return (
            cls.quits(date)
            .where(cls.subscription_type == SubscriptionType.INDIVIDUAL)
            .count()
        )

    @classmethod
    def churn_ptc(cls, date):
        from_date = month_range(date)[0]
        churn = cls.quits_count(date) / (
            cls.active_count(from_date) + cls.signups_count(date)
        )
        return churn * 100

    @classmethod
    @uses_data_from_subscriptions()
    def individuals_churn_ptc(cls, date):
        from_date = month_range(date)[0]
        churn = cls.individuals_quits_count(date) / (
            cls.active_individuals_count(from_date)
            + cls.individuals_signups_count(date)
        )
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
        account_ids = [
            activity.account_id for activity in cls.active_individuals_listing(date)
        ]
        if durations := list(cls._calc_durations(account_ids, date)):
            return sum(durations) / len(durations)
        return 0

    @classmethod
    def _calc_durations(
        cls, account_ids: list[str], date: date
    ) -> Generator[int, None, None]:
        earliest_on = fn.min(cls.happened_on).alias("earliest_on")
        items = (
            cls.select(earliest_on)
            .where(cls.account_id.in_(account_ids))
            .group_by(cls.account_id)
            .dicts()
        )
        for item in items:
            duration_sec = (date - item["earliest_on"]).total_seconds()
            duration_mo = duration_sec / 60 / 60 / 24 / 30
            yield duration_mo

    @classmethod
    def account_listing(cls, account_id: int) -> Iterable[Self]:
        return (
            cls.select().where(cls.account_id == account_id).order_by(cls.happened_at)
        )

    @classmethod
    def account_subscribed_at(cls, account_id: int) -> datetime | None:
        first_activity = cls.account_listing(account_id).first()
        if first_activity:
            return first_activity.happened_at

    @classmethod
    def account_subscribed_days(cls, account_id: int, today: date = None) -> int:
        days = 0
        today = today or date.today()
        start = None
        for activity in cls.account_listing(account_id):
            if activity.type == SubscriptionActivityType.DEACTIVATION:
                if start:
                    days += (
                        activity.happened_at.date() - start.happened_at.date()
                    ).days
                    start = None
            elif start is None:
                start = activity
        if start:
            days += (today - start.happened_at.date()).days
        return days


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
