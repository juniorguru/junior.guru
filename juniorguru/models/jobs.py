from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


class SetField(CharField):
    def db_value(self, python_value):
        assert all(';' not in item for item in python_value)
        return ';'.join(sorted(python_value))

    def python_value(self, db_value):
        return frozenset(db_value.split(';'))


class Job(BaseModel):
    id = CharField(primary_key=True)
    timestamp = DateTimeField(index=True)
    company_name = CharField()
    job_type = CharField()
    title = CharField()
    company_link = CharField()
    email = CharField()
    location = CharField(index=True)
    description = CharField()
    requirements = SetField()
    is_approved = BooleanField(default=False, index=True)

    @classmethod
    def listing(cls):
        return Job.select() \
            .where(Job.is_approved == True) \
            .order_by(Job.timestamp.desc())

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(set([job.company_link for job in cls.listing()]))
