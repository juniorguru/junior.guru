import pytest

from juniorguru.jobs.employments.pipelines.identify import Pipeline, MissingIdentifyingField, parse_id


def test_identify(item, spider):
    item['url'] = 'https://www.startupjobs.cz/nabidka/11067/junior-programator-python'
    item = Pipeline().process_item(item, spider)

    assert item['external_ids'] == ['startupjobs#11067']


def test_identify_unique(item, spider):
    item['url'] = 'https://www.startupjobs.cz/nabidka/11067/junior-programator-python'
    item['apply_url'] = 'https://www.startupjobs.cz/nabidka/11067/junior-programator-python?utm_source=juniorguru'
    item = Pipeline().process_item(item, spider)

    assert item['external_ids'] == ['startupjobs#11067']


def test_identify_sorted(item, spider):
    item['url'] = 'https://junior.guru/jobs/215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921/'
    item['apply_url'] = 'https://www.startupjobs.cz/nabidka/11067/junior-programator-python?utm_source=juniorguru'
    item = Pipeline().process_item(item, spider)

    assert item['external_ids'] == ['juniorguru#215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921', 'startupjobs#11067']

    item['url'] = 'https://www.startupjobs.cz/nabidka/11067/junior-programator-python?utm_source=juniorguru'
    item['apply_url'] = 'https://junior.guru/jobs/215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921/'
    item = Pipeline().process_item(item, spider)

    assert item['external_ids'] == ['juniorguru#215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921', 'startupjobs#11067']


def test_identify_raises(item, spider):
    del item['url']
    with pytest.raises(MissingIdentifyingField):
        Pipeline().process_item(item, spider)


@pytest.mark.parametrize('url, expected', [
    ('https://example.com',
     None),
    ('https://www.startupjobs.cz/nabidka/11067/junior-programator-python?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru',
     'startupjobs#11067'),
    ('https://cz.linkedin.com/jobs/view/junior-mobile-developer-at-komer%C4%8Dn%C3%AD-banka-2533120346',
     'linkedin#2533120346'),
    ('https://stackoverflow.com/jobs/548716/junior-engineer-australia-new-zealand-octopus-deploy',
     'stackoverflow#548716'),
    ('https://remoteOK.io/remote-jobs/106090-remote-senior-software-engineer-cloud-platform-lucidworks-remote-senior-software-engineer-cloud-platform-lucidworks',
     'remoteok#106090'),
    ('https://weworkremotely.com/remote-jobs/exavault-inc-senior-devops-engineer-1-pb-storage',
     'weworkremotely#exavault-inc-senior-devops-engineer-1-pb-storage'),
    ('https://junior.guru/jobs/215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921/',
     'juniorguru#215426887eaaad9105ecf647d0ff24cf94de7c9eb47cc6f2c55e6921'),
])
def test_parse_id(url, expected):
    assert parse_id(url) == expected
