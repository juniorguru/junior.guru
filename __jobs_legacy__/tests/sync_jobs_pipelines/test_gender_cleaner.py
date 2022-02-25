import pytest

from juniorguru.jobs.legacy_jobs.pipelines.gender_cleaner import Pipeline


@pytest.mark.parametrize('title,expected', [
    # German
    ('Full Stack Software Engineer: Ruby on Rails (m/f/d)',
     'Full Stack Software Engineer: Ruby on Rails'),
    ('Full Stack Software Engineer: Java / Python (m/f/d)',
     'Full Stack Software Engineer: Java / Python'),
    ('Quantitative Java Developer (m/f/d) for Financial Markets',
     'Quantitative Java Developer for Financial Markets'),
    ('Search Engine Backend Engineer (m/f)',
     'Search Engine Backend Engineer'),
    ('Computer scientist - Software Architectures for Traffic Systems (f/m/d)',
     'Computer scientist - Software Architectures for Traffic Systems'),
    ('JAVA BPM SOFTWARE DEVELOPER (M/F)',
     'JAVA BPM SOFTWARE DEVELOPER'),
    ('Frontend Engineer (m/f/div)',
     'Frontend Engineer'),
    ('Junior Fullstack Developer (m/w/d)',
     'Junior Fullstack Developer'),
    ('Java Developer (m/w)',
     'Java Developer'),
    ('Software Engineer Ruby/Go (f/m/*)',
     'Software Engineer Ruby/Go'),
    ('C/Ada Software Developer & Tester Aviation (m/f/d )(Ref.-Nr.: 2020)',
     'C/Ada Software Developer & Tester Aviation (Ref.-Nr.: 2020)'),
    ('Solution Engineer (M/F/X)',
     'Solution Engineer'),
    ('UI Frontend Engineer | React JS Developer f/m/x',
     'UI Frontend Engineer | React JS Developer'),
    ('Junior iOS Engineer (Swift) (m|f|x)',
     'Junior iOS Engineer (Swift)'),
    ('Archer Developer (m/f/diverse)',
     'Archer Developer'),
    ('Tech Trainee Programme (Java-JavaScript-iOS-Android) (d/f/m)',
     'Tech Trainee Programme (Java-JavaScript-iOS-Android)'),

    # French
    ('Internship: JAVA DEVELOPER - H/F',
     'Internship: JAVA DEVELOPER'),

    # Czech
    ('GOlang / PHP backend programátor cloudových služeb (m/ž)',
     'GOlang / PHP backend programátor cloudových služeb'),
    ('👩‍💻/👨‍💻 Junior Product Designer',
     'Junior Product Designer')
])
def test_gender_cleaner(item, spider, title, expected):
    item['title'] = title
    item = Pipeline().process_item(item, spider)

    assert item['title'] == expected
