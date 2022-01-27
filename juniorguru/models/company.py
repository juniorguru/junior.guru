from datetime import date

from peewee import CharField, DateField, BooleanField, IntegerField

from juniorguru.models.base import BaseModel
from juniorguru.models import ClubUser


class Company(BaseModel):
    name = CharField()
    filename = CharField()
    is_sponsoring_handbook = BooleanField(default=False)
    link = CharField()
    coupon = CharField(null=True)
    student_coupon = CharField(null=True)
    starts_at = DateField(null=True)
    expires_at = DateField(null=True)
    role_id = IntegerField(null=True)
    student_role_id = IntegerField(null=True)

    @property
    def list_employees(self):
        if not self.coupon:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon == self.__class__.coupon)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon == self.coupon))

    @property
    def list_students(self):
        if not self.student_coupon:
            return []
        return ClubUser.select() \
            .join(self.__class__, on=(ClubUser.coupon == self.__class__.student_coupon)) \
            .where((ClubUser.is_member == True) & (ClubUser.coupon == self.student_coupon))

    @classmethod
    def listing(cls, today=None):
        today = today or date.today()
        return cls.select() \
            .where(cls.starts_at <= today,
                   (cls.expires_at >= today) | cls.expires_at.is_null()) \
            .order_by(cls.starts_at, cls.name)

    @classmethod
    def handbook_listing(cls, today=None):
        today = today or date.today()
        return cls.listing() \
            .where(cls.is_sponsoring_handbook == True)

    @classmethod
    def students_listing(cls):
        return cls.listing() \
            .where(cls.student_coupon.is_null(False))
