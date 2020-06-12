from peewee import CharField, DateField, DateTimeField, IntegerField, TextField

from juniorguru.models.base import BaseModel, JSONField


class UniqueSortedListField(CharField):
    def db_value(self, python_value):
        assert all(';' not in item for item in python_value)
        return ';'.join(self._sort(frozenset(python_value)))

    def python_value(self, db_value):
        return db_value.split(';')

    def _sort(self, iterable):
        return sorted(iterable)


class EmploymentTypeField(UniqueSortedListField):
    known_types_sorted = [
        'full-time',
        'part-time',
        'contract',
        'paid internship',
        'unpaid internship',
        'internship',
        'volunteering',
    ]

    def _key(self, item):
        if item in self.known_types_sorted:
            return (self.known_types_sorted.index(item), '')
        return (1000, item)

    def _sort(self, iterable):
        return sorted(iterable, key=self._key)


class Job(BaseModel):
    id = CharField(primary_key=True)
    posted_at = DateTimeField(index=True)
    title = CharField()
    location = CharField()
    company_name = CharField()
    company_link = CharField(null=True)  # required for JG
    employment_types = EmploymentTypeField()
    link = CharField(null=True, index=True)  # required for scraped
    source = CharField()

    # only set by JG
    email = CharField(null=True)  # required for JG
    description = TextField(null=True)  # required for JG
    approved_at = DateField(null=True)
    expires_at = DateField(null=True)
    newsletter_at = DateField(null=True)

    # only set by scraped
    lang = CharField(null=True)  # required for scraped
    jg_rank = IntegerField(null=True)  # required for scraped
    response_url = CharField(null=True)  # required for scraped
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)  # required for scraped

    # See job_attrs.py for the rest of the model definition. It's done this
    # way because of circular dependencies between Job and JobMetric
    # https://stackoverflow.com/q/62327182/325365


class JobDropped(BaseModel):
    type = CharField()
    reason = CharField()
    response_url = CharField()
    response_backup_path = CharField(null=True)
    item = JSONField()

    @classmethod
    def admin_listing(cls):
        return cls.select().order_by(cls.type, cls.reason)


class JobError(BaseModel):
    message = CharField()
    trace = CharField()
    signal = CharField(choices=(('item', None), ('spider', None)))
    spider = CharField()
    response_url = CharField()
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)

    @classmethod
    def admin_listing(cls):
        return cls.select().order_by(cls.message)
