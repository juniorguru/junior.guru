import pytest

from juniorguru.scrapers.pipelines.employment_types_cleaner import Pipeline


@pytest.mark.parametrize('employment_types,expected', [
    # common sense
    (['fulltime'], ['full-time']),
    (['full time'], ['full-time']),
    (['parttime'], ['part-time']),
    (['part time'], ['part-time']),

    # StackOverflow
    (['Full-time'], ['full-time']),
    (['Internship'], ['internship']),
    (['Contract'], ['contract']),

    # StartupJobs
    (['external collaboration'], ['contract']),

    # processing an unknown employment type
    (['Full-Time', 'Gargamel'], ['full-time', 'gargamel']),
    (['Gargamel'], ['gargamel']),

    # processing duplicates
    (['Full-Time', 'Gargamel', 'full time'], ['full-time', 'gargamel']),
])
def test_employment_types_cleaner(item, spider, employment_types, expected):
    item['employment_types'] = employment_types
    item = Pipeline().process_item(item, spider)

    assert sorted(item['employment_types']) == sorted(expected)
