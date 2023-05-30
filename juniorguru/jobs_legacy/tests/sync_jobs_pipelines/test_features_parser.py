from juniorguru.jobs.legacy_jobs.pipelines.features_parser import Pipeline, deduplicate


def test_features_parser(item, spider):
    item['lang'] = 'en'
    item['title'] = 'Senior C# Developer'
    item['description_sentences'] = ['5 years experience with C#']
    item = Pipeline().process_item(item, spider)

    assert item['features'][0] == dict(name='ENGLISH_REQUIRED',
                                       origin='language_filter')
    assert item['features'][1]['name'] == 'EXPLICITLY_SENIOR'
    assert item['features'][1]['origin'] == 'features_parser'
    assert item['features'][1]['sentence'] == 'Senior C# Developer'
    assert len(item['features'][1]['patterns']) >= 1
    assert item['features'][2]['name'] == 'YEARS_EXPERIENCE_REQUIRED'
    assert item['features'][2]['origin'] == 'features_parser'
    assert item['features'][2]['sentence'] == '5 years experience with C#'
    assert len(item['features'][2]['patterns']) >= 1


def test_deduplicate():
    assert deduplicate([
        ('ADVANCED_REQUIRED', 'you need very advanced English', r'advanced'),
        ('ADVANCED_REQUIRED', 'you need very advanced English', r'be very'),
        ('ENGLISH_REQUIRED', 'you need very advanced English', r'english'),
        ('ADVANCED_REQUIRED', 'different sentence', r'advanced'),
    ]) == [
        ('ADVANCED_REQUIRED', 'you need very advanced English', [r'advanced', r'be very']),
        ('ENGLISH_REQUIRED', 'you need very advanced English', [r'english']),
        ('ADVANCED_REQUIRED', 'different sentence', [r'advanced']),
    ]
