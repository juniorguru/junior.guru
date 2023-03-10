import pytest

from juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner import process, clean_employment_type, clean_employment_types


@pytest.mark.parametrize('employment_type, expected', [
    # common sense
    ('fulltime', 'FULL_TIME'),
    ('full time', 'FULL_TIME'),
    ('parttime', 'PART_TIME'),
    ('part time', 'PART_TIME'),

    # StackOverflow
    ('Full-time', 'FULL_TIME'),
    ('Internship', 'INTERNSHIP'),
    ('Contract', 'CONTRACT'),

    # StartupJobs
    ('external collaboration', 'CONTRACT'),

    # Jobs
    ('full-time work', 'FULL_TIME'),
    ('práce na plný úvazek', 'FULL_TIME'),
    ('part-time work', 'PART_TIME'),
    ('práce na zkrácený úvazek', 'PART_TIME'),

    # junior.guru
    ('paid internship', 'PAID_INTERNSHIP'),
    ('unpaid internship', 'UNPAID_INTERNSHIP'),
    ('internship', 'INTERNSHIP'),
    ('volunteering', 'VOLUNTEERING'),
    ('plný úvazek', 'FULL_TIME'),
    ('částečný úvazek', 'PART_TIME'),
    ('placená stáž', 'PAID_INTERNSHIP'),
    ('neplacená stáž', 'UNPAID_INTERNSHIP'),
    ('stáž', 'INTERNSHIP'),
    ('dobrovolnictví', 'VOLUNTEERING'),

    # removing an unknown employment type
    ('Gargamel', None),
])
def test_employment_types_cleaner_clean_employment_type(employment_type, expected):
    assert clean_employment_type(employment_type) == expected


@pytest.mark.parametrize('item, expected', [
    (dict(employment_types=['Full-Time']), dict(employment_types=['FULL_TIME'])),
    (dict(employment_types=['part time', 'Full-Time']), dict(employment_types=['FULL_TIME', 'PART_TIME'])),
    (dict(), dict()),
])
def test_employment_types_cleaner(item, expected):
    item = process(item)

    assert item == expected


@pytest.mark.parametrize('employment_types, expected', [
    (['Full-Time', 'Gargamel'], ['FULL_TIME']),
    (['Gargamel'], []),
    (['Full-Time', 'Gargamel', 'full time'], ['FULL_TIME']),
])
def test_employment_types_cleaner_clean_employment_types(employment_types, expected):
    assert clean_employment_types(employment_types) == expected
