from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


class Job(BaseModel):
    id = CharField(primary_key=True)
    timestamp = DateTimeField(index=True)
    title = CharField()
    location = CharField()
    company_name = CharField()
    company_link = CharField()
    email = CharField()
    job_type = CharField()
    description = CharField()
    is_approved = BooleanField(default=False)
    is_sent = BooleanField(default=False)

    @classmethod
    def listing(cls):
        return Job.select() \
            .where(Job.is_approved == True) \
            .order_by(Job.timestamp.desc())

    @classmethod
    def newsletter_listing(cls):
        return Job.select() \
            .where(Job.is_approved == True, Job.is_sent == False) \
            .order_by(Job.timestamp)

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(set([job.company_link for job in cls.listing()]))
