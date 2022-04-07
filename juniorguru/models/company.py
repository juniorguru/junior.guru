from datetime import date

from peewee import BooleanField, CharField, DateField, ForeignKeyField, IntegerField

from juniorguru.models.base import BaseModel
from juniorguru.models.club import ClubUser


class Company(BaseModel):
    name = CharField()
    slug = CharField(null=True, unique=True)
    logo_filename = CharField()
    is_sponsoring_handbook = BooleanField(default=False)
    url = CharField()
    coupon_base = CharField(null=True)
    student_coupon_base = CharField(null=True)
    job_slots_count = IntegerField(default=0)
    starts_on = DateField()
    expires_on = DateField(null=True)
    role_id = IntegerField(null=True)
    student_role_id = IntegerField(null=True)
    poster_path = CharField(null=True)

    @property
    def is_school(self):
        return bool(self.student_coupon_base)

    @property
    def list_members(self):
        if not self.coupon_base:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon_base == self.__class__.coupon_base)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon_base == self.coupon_base))

    @property
    def list_student_members(self):
        if not self.student_coupon_base:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon_base == self.__class__.student_coupon_base)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon_base == self.student_coupon_base))

    @property
    def list_student_subscriptions_billable(self):
        return self.list_student_subscriptions \
            .where(CompanyStudentSubscription.invoiced_on.is_null())

    @classmethod
    def get_by_slug(cls, slug):
        if not slug:
            raise ValueError(repr(slug))
        return cls.select() \
            .where(cls.slug == slug) \
            .get()

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.starts_on <= today,
                   (cls.expires_on >= today) | cls.expires_on.is_null()) \
            .order_by(cls.starts_on, cls.name)

    @classmethod
    def handbook_listing(cls, today=None):
        today = today or date.today()
        return cls.listing() \
            .where(cls.is_sponsoring_handbook == True)

    @classmethod
    def schools_listing(cls):
        return cls.listing() \
            .where(cls.student_coupon_base.is_null(False))

    def __str__(self):
        return self.name


class CompanyStudentSubscription(BaseModel):
    company = ForeignKeyField(Company, backref='list_student_subscriptions')
    memberful_id = CharField()
    name = CharField()
    email = CharField()
    started_on = DateField()
    invoiced_on = DateField(null=True)

    def __str__(self):
        return f'{self.company.slug}, #{self.memberful_id}, {self.started_on}, {self.invoiced_on}'
