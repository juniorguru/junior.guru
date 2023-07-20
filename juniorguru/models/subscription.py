from datetime import date
from enum import StrEnum, unique

from peewee import BooleanField, CharField, DateTimeField

from juniorguru.models.base import BaseModel, check_enum


LEGACY_PLANS_DELETED_ON = date(2023, 2, 24)


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


class SubscriptionActivity(BaseModel):
    class Meta:
        indexes = (
            (('type', 'account_id', 'happened_at'), True),
        )

    type = CharField()
    account_id = CharField(index=True)
    account_has_feminine_name = BooleanField()
    happened_at = DateTimeField(index=True)
    order_coupon = CharField(null=True)
    subscription_interval = CharField(null=True, constraints=[check_enum('subscription_interval', SubscriptionInterval)])
    subscription_type = CharField(null=True, constraints=[check_enum('subscription_type', SubscriptionType)])

    @classmethod
    def add(cls, **kwargs):
        unique_key_fields = cls._meta.indexes[0][0]
        if set(unique_key_fields) == set(kwargs.keys()) or not any(kwargs.values()):
            insert = cls.insert(**kwargs) \
                .on_conflict_ignore()
        else:
            conflict_target = [getattr(cls, field) for field in unique_key_fields]
            update = {field: kwargs[field]
                      for field, value in kwargs.items()
                      if ((value is not None) and
                          (field not in unique_key_fields))}
            insert = cls.insert(**kwargs) \
                .on_conflict(action='update',
                             update=update,
                             conflict_target=conflict_target)
        insert.execute()

    @classmethod
    def cleanup(cls):
        cls_also = cls.alias()

        # Trials which are part of a free subscription are not really trials
        cls.delete() \
            .where(cls.type.in_(['trial_start', 'trial_end']),
                   cls.subscription_type == SubscriptionType.FREE) \
            .execute()

        # Activating trial also creates an 'order' activity.
        # We want to keep only the 'trial_start' activity so that
        # 'order' activites only mark moments where money is involved.
        to_delete = cls.select(cls.id) \
            .join(cls_also, on=((cls.account_id == cls_also.account_id) &
                                (cls.happened_at == cls_also.happened_at))) \
            .where(cls.type == 'order', cls_also.type == 'trial_start')
        cls.delete().where(cls.id.in_(to_delete)).execute()

    @classmethod
    def count(cls):
        return cls.select().count()


class SubscriptionCancellation(BaseModel):
    name = CharField()
    email = CharField()
    reason = CharField()
    feedback = CharField(null=True)


class SubscriptionReferrer(BaseModel):
    account_id = CharField()
    name = CharField()
    email = CharField()
    referrer = CharField()


class SubscriptionOrigin(BaseModel):
    account_id = CharField()
    name = CharField()
    email = CharField()
    origin = CharField()


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

#     def __str__(self):
#         return f'#{self.account_id} {self.start_on}…{self.end_on} {self.type}'
