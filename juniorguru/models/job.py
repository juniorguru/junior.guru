from peewee import BooleanField, CharField, DateTimeField

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
    email = CharField(null=True)  # required for JG, null for scraped
    employment_types = EmploymentTypeField()
    description = CharField(null=True)  # required for JG, null for scraped
    lang = CharField(null=True)  # required for scraped, null for JG
    link = CharField(null=True)  # required for scraped
    source = CharField()
    is_approved = BooleanField(default=False)
    is_sent = BooleanField(default=False)
    is_expired = BooleanField(default=False)
    response_url = CharField(null=True)  # required for scraped, null for JG
    response_backup_path = CharField(null=True)
    item = JSONField(null=True)  # required for scraped, null for JG

    @classmethod
    def listing(cls):
        return cls.juniorguru_listing()

    @classmethod
    def newsletter_listing(cls):
        return cls.select() \
            .where(cls.is_approved == True,
                   cls.is_expired == False,
                   cls.is_sent == False) \
            .order_by(cls.posted_at)

    @classmethod
    def juniorguru_listing(cls):
        return cls.select() \
            .where(cls.source == 'juniorguru',
                   cls.is_approved == True,
                   cls.is_expired == False) \
            .order_by(cls.posted_at.desc())

    @classmethod
    def scraped_listing(cls):
        return cls.select() \
            .where(cls.source != 'juniorguru') \
            .order_by(cls.posted_at.desc())

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(frozenset([job.company_link for job in cls.listing()]))


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
