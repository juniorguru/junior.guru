from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from scrapy import Spider
from peewee import SqliteDatabase

from juniorguru.scrapers import pipelines
from juniorguru.models import Job


@pytest.fixture
def item():
    return dict(
        posted_at=datetime.utcnow(),
        title='Junior Python Engineer',
        location='Brno, Czechia',
        company_name='The Best Company',
        company_link='https://example.com',
        employment_types=['full-time'],
        description_raw='...',
        link='https://example.com/jobs/123',
    )


@pytest.fixture
def spider():
    class DummySpider(Spider):
        name = 'dummy'

    return DummySpider()


@pytest.mark.parametrize('title', [
    '(Senior) Python Developer Backend – Billing / Product',
    'practiced .NET Developer',
])
def test_junior_title_filter(item, spider, title):
    item['title'] = title
    pipeline = pipelines.JuniorTitleFilter()

    with pytest.raises(pipelines.BannedWordInTitle):
        pipeline.process_item(item, spider)


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

    # processing an unknown employment type
    (['Full-Time', 'Gargamel'], ['full-time', 'gargamel']),
    (['Gargamel'], ['gargamel']),

    # processing duplicates
    (['Full-Time', 'Gargamel', 'full time'], ['full-time', 'gargamel']),
])
def test_employment_types_cleaner(item, spider, employment_types, expected):
    item['employment_types'] = employment_types
    pipeline = pipelines.EmploymentTypesCleaner()
    item = pipeline.process_item(item, spider)

    assert sorted(item['employment_types']) == sorted(expected)


@pytest.mark.parametrize('title,expected', [
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
])
def test_german_gender_cleaner(item, spider, title, expected):
    item['title'] = title
    pipeline = pipelines.GermanGenderCleaner()
    item = pipeline.process_item(item, spider)

    assert item['title'] == expected


@pytest.mark.parametrize('description_raw,expected_lang', [
    ('''<p>Baví nás e-commerce a proto jsme se před rokem pustili do tvorby
     aplikací pro <a href="https://www.shopify.com/">Shopify.com</a>.
     Provozujeme více aplikací, např. Candyrack, zaměřené na performance
     marketing a dnes je využívají stovky e-shopů z celého světa.</p>''',
     'cs'),
    ('''V súčasnosti hľadáme inžiniera zameraného na cloud, pre spoločnosť
     špecializujúcou sa na poisťovníctvo na svojom trhu na Slovensku,
     spoločnosť pôsobí okrem Slovenska vo viacerých krajinách sveta.''',
     'sk'),
    ('''Help companies that use the Prague-based AI startup
     <strong>Rossum</strong> get started (...to stop wasting time on manual
     data entry when dealing with business documents).''',
     'en'),
])
def test_language_filter(item, spider, description_raw, expected_lang):
    item['description_raw'] = description_raw
    pipeline = pipelines.LanguageFilter()
    item = pipeline.process_item(item, spider)

    assert item['lang'] == expected_lang


@pytest.mark.parametrize('description_raw', [
    '''<p><strong>Was dich\xa0bei uns erwartet:\xa0</strong></p>\r\n<p>Als
    Big Data Systems Engineer bist du bei unseren Kunden für die Konzeption,
    Installation und Konfiguration der Linux- und Cloud-basierten
    Big-Data-Lösungen verantwortlich. Ebenfalls zu deinen Aufgaben gehören
    die Bewertung bestehender Big-Data-Systeme und die''',
    '''<div class="f1header">Na tym stanowisku będziesz odpowiedzialna/-y za:
    </div><ul><li>przeprowadzanie testów manualnych i automatycznych</li><li>
    raportowanie błędów</li>''',
])
def test_language_filter_drops(item, spider, description_raw):
    item['description_raw'] = description_raw
    pipeline = pipelines.LanguageFilter()

    with pytest.raises(pipelines.IrrelevantLanguage):
        pipeline.process_item(item, spider)


@pytest.fixture
def db():
    # Using tmp file because we need to test opening and closing a db conn
    # here and the :memory: sqlite db ceases to exist with the conn closed
    tmp_file = NamedTemporaryFile(delete=False)
    db_path = Path(tmp_file.name)
    tmp_file.close()
    db = SqliteDatabase(tmp_file.name)
    with db:
        Job.bind(db)
        Job.create_table()
    yield db
    if db_path.exists():
        db_path.unlink()


def test_database(item, spider, db):
    pipeline = pipelines.Database(db=db, job_cls=Job)
    pipeline.open_spider(spider)
    pipeline.process_item(item, spider)
    pipeline.close_spider(spider)
    with db:
        job = Job.select()[0]

    assert len(job.id) == 56  # sha224 hex digest length
    assert job.source == 'dummy'  # spider name
    assert job.is_approved is False
