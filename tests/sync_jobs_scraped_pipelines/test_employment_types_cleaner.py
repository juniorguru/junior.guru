import pytest

from juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner import process


@pytest.mark.parametrize('employment_types, expected', [
    # common sense
    (['fulltime'], ['FULL_TIME']),
    (['full time'], ['FULL_TIME']),
    (['parttime'], ['PART_TIME']),
    (['part time'], ['PART_TIME']),

    # StackOverflow
    (['Full-time'], ['FULL_TIME']),
    (['Internship'], ['INTERNSHIP']),
    (['Contract'], ['CONTRACT']),

    # StartupJobs
    (['external collaboration'], ['CONTRACT']),

    # Jobs
    (['full-time work'], ['FULL_TIME']),
    (['práce na plný úvazek'], ['FULL_TIME']),
    (['part-time work'], ['PART_TIME']),
    (['práce na zkrácený úvazek'], ['PART_TIME']),

    # junior.guru
    (['paid internship'], ['PAID_INTERNSHIP']),
    (['unpaid internship'], ['UNPAID_INTERNSHIP']),
    (['internship'], ['INTERNSHIP']),
    (['volunteering'], ['VOLUNTEERING']),
    (['plný úvazek'], ['FULL_TIME']),
    (['částečný úvazek'], ['PART_TIME']),
    (['placená stáž'], ['PAID_INTERNSHIP']),
    (['neplacená stáž'], ['UNPAID_INTERNSHIP']),
    (['stáž'], ['INTERNSHIP']),
    (['dobrovolnictví'], ['VOLUNTEERING']),

    # removing an unknown employment type
    (['Full-Time', 'Gargamel'], ['FULL_TIME']),
    (['Gargamel'], []),

    # processing duplicates
    (['Full-Time', 'Gargamel', 'full time'], ['FULL_TIME']),
])
def test_employment_types_cleaner(employment_types, expected):
    item = process(dict(employment_types=employment_types))

    assert sorted(item['employment_types']) == sorted(expected)


def test_employment_types_cleaner_no_employment_types():
    item = process(dict())

    assert 'employment_types' not in item
