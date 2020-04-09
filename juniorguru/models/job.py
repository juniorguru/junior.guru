from peewee import DateTimeField, CharField, BooleanField

from .base import BaseModel


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
    timestamp = DateTimeField(index=True)
    title = CharField()
    location = CharField()
    company_name = CharField()
    company_link = CharField()
    email = CharField()
    employment_types = EmploymentTypeField()
    description = CharField()
    link = CharField(null=True)
    is_approved = BooleanField(default=False)
    is_sent = BooleanField(default=False)
    is_expired = BooleanField(default=False)

    @classmethod
    def listing(cls):
        return cls.select() \
            .where(cls.is_approved == True,
                   cls.is_expired == False) \
            .order_by(cls.timestamp.desc())

    @classmethod
    def newsletter_listing(cls):
        return cls.select() \
            .where(cls.is_approved == True,
                   cls.is_expired == False,
                   cls.is_sent == False) \
            .order_by(cls.timestamp)

    @classmethod
    def count(cls):
        return cls.listing().count()

    @classmethod
    def companies_count(cls):
        return len(set([job.company_link for job in cls.listing()]))
