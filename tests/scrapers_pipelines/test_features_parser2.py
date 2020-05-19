import pytest

from juniorguru.scrapers.pipelines.features_parser2 import parse_from_sentence


@pytest.mark.parametrize('sentence,expected', [
    ('10+ experience with architecting', 'YEARS_EXPERIENCE_REQUIRED'),
    ('10+ experience with architecting', 'ADVANCED_REQUIRED'),
    ('developer with strong technical background', 'ADVANCED_REQUIRED'),
    ('We are looking for a seasoned engineer', 'ADVANCED_REQUIRED'),
    ('engineer with a thorough understanding', 'ADVANCED_REQUIRED'),
    ('At least 5 years’ experience as an iOS mobile developer.', 'YEARS_EXPERIENCE_REQUIRED'),
    ('Experience leading a team', 'LEADERSHIP_REQUIRED'),
    ('Lead a growing team', 'LEADERSHIP_REQUIRED'),
    ('Czech/Slovak language knowledge/possibly is essential', 'CZECH_REQUIRED'),
    ('Czech/Slovak language knowledge/possibly is essential', 'SLOVAK_REQUIRED'),
    ('have Computing Degree', 'DEGREE_REQUIRED'),
    ('experienced Java developer', 'ADVANCED_REQUIRED'),
    ('Although team language is Czech - basic English knowledge is required', 'CZECH_REQUIRED'),
    ('strong Java development background', 'ADVANCED_REQUIRED'),
    ('execute tasks independently', 'INDEPENDENCE_REQUIRED'),
    ('with little supervision and under pressure', 'INDEPENDENCE_REQUIRED'),
    ('Two or more years of hands-on experience', 'YEARS_EXPERIENCE_REQUIRED'),
    ('You have a degree in Computer Science, Mathematics, Physics or Business Administration.', 'DEGREE_REQUIRED'),
    ('working experience in (software) development', 'ADVANCED_REQUIRED'),
    ('Excellent analytical and problem-solving skills', 'ADVANCED_REQUIRED'),
    ('Able to work with minimal supervision', 'INDEPENDENCE_REQUIRED'),
    ('Solid technical background', 'ADVANCED_REQUIRED'),
    ('work independently on given tasks', 'INDEPENDENCE_REQUIRED'),
    ('Proven commercial experience working with Java', 'ADVANCED_REQUIRED'),
    ('sound knowledge of HTML', 'ADVANCED_REQUIRED'),
    ('Strong experience (5+ years) in Java', 'YEARS_EXPERIENCE_REQUIRED'),
    ('previous experience in C++', 'ADVANCED_REQUIRED'),
    ('significant technical background', 'ADVANCED_REQUIRED'),
    ('work autonomously on given tasks', 'INDEPENDENCE_REQUIRED'),
    ('very solid know-how on how to write C++', 'ADVANCED_REQUIRED'),
    ('take responsibility for good architecture and software design', 'ADVANCED_REQUIRED'),
    ('After your studies in mathematics, computer science, engineering, business or comparable studies', 'DEGREE_REQUIRED'),
    ('you have gained professional experience', 'ADVANCED_REQUIRED'),
    ('Very good programming skills and practical experience', 'ADVANCED_REQUIRED'),
    ('Completed technical education (college or university level)', 'DEGREE_REQUIRED'),
    ('experience in building very complex applications', 'ADVANCED_REQUIRED'),
    ('Independent working ability', 'INDEPENDENCE_REQUIRED'),
    ('Bachelor’s degree or higher (min A- average for under-graduate, first class for post-graduate).', 'DEGREE_REQUIRED'),
    ('Independent, self-directing working style.', 'INDEPENDENCE_REQUIRED'),
    ('experience as a Technical Leader', 'LEADERSHIP_REQUIRED'),
    ('leadership skills', 'LEADERSHIP_REQUIRED'),
    ('Leadership experience', 'LEADERSHIP_REQUIRED'),
])
def test_parse_from_sentence_en(sentence, expected):
    features = list(parse_from_sentence(sentence, 'en'))
    feature_ids = {feature_id for feature_id, sentence, pattern in features}

    assert expected in feature_ids


@pytest.mark.parametrize('sentence,not_expected', [
    ('Good english communication skills', 'ADVANCED_REQUIRED'),
    ('completed training in computer science / electrical engineering', 'DEGREE_REQUIRED'),
    ('BS or MS in software engineering or equivalent experience', 'DEGREE_REQUIRED'),
])
def test_parse_from_sentence_en_suppressed(sentence, not_expected):
    features = list(parse_from_sentence(sentence, 'en'))
    feature_ids = {feature_id for feature_id, sentence, pattern in features}

    assert not_expected not in feature_ids


# TODO
[
    'AJ minimálně na úrovni technické specifikace',
    'Angličtinu minimálně na úrovni technické specifikace',
    'Vzdělání:vyšší odborné, SŠ s maturitou, bakalářské, vysokoškolské',
    'SŠ/VŠ vzdělání technického zaměření'
    'Znalost problematiky programování webových aplikací (min. 3 roky)'
]


# TODO context
# !!!
# 7a081488f0f6b53d28c4bc4d8fc2801972bd5e21d9b5756fed9636f5

# 'Nice to Have',
# 'Completed studies in computer science',
