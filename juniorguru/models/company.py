from datetime import date

from peewee import CharField, DateField, BooleanField, IntegerField

from juniorguru.models.base import BaseModel
from juniorguru.models import ClubUser


class Company(BaseModel):
    name = CharField()
    logo_filename = CharField()
    is_sponsoring_handbook = BooleanField(default=False)
    link = CharField()
    coupon_base = CharField(null=True)
    student_coupon_base = CharField(null=True)
    starts_on = DateField(null=True)
    expires_on = DateField(null=True)
    role_id = IntegerField(null=True)
    student_role_id = IntegerField(null=True)

    @property
    def list_employees(self):
        if not self.coupon_base:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon_base == self.__class__.coupon_base)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon_base == self.coupon_base))

    @property
    def list_students(self):
        if not self.student_coupon_base:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon_base == self.__class__.student_coupon_base)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon_base == self.student_coupon_base))

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
    def students_listing(cls):
        return cls.listing() \
            .where(cls.student_coupon_base.is_null(False))
