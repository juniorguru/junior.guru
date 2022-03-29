import pytest

from juniorguru.jobs.legacy_jobs.pipelines.employment_types_cleaner import Pipeline


@pytest.mark.parametrize('employment_types,expected', [
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
def test_employment_types_cleaner(item, spider, employment_types, expected):
    item['employment_types'] = employment_types
    item = Pipeline().process_item(item, spider)

    assert sorted(item['employment_types']) == sorted(expected)


def test_employment_types_cleaner_no_employment_types(item, spider):
    if 'employment_types' in item:
        del item['employment_types']
    item = Pipeline().process_item(item, spider)

    assert 'employment_types' not in item
