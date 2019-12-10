from textwrap import dedent
from datetime import datetime

import pytest

from juniorguru.web import template_filters


def test_email_link():
    markup = str(template_filters.email_link('xyz@example.com'))
    assert markup == '<a href="mailto:xyz&#64;example.com">xyz&#64;<!---->example.com</a>'


def test_md():
    markup = str(template_filters.md('call me **maybe**  \ncall me Honza'))
    assert markup == '<p>call me <strong>maybe</strong><br>\ncall me Honza</p>'


def test_md_heading_level_base():
    markup = str(template_filters.md(dedent('''
        # Heading 1
        ## Heading 2
        Paragraph text
    '''), heading_level_base=4)).strip()
    assert markup == dedent('''
        <h4 id="heading-1">Heading 1</h4>
        <h5 id="heading-2">Heading 2</h5>
        <p>Paragraph text</p>
    ''').strip()


@pytest.mark.parametrize('requirement,expected', [
    ('mainstream programming language', 'základy programování'),
    ('databases', 'databáze'),
    ('data analysis', 'datová analýza'),
    ('servers and operations', 'správa serverů'),
    ('web backend', 'webový backend'),
    ('web frontend', 'webový frontend'),
    ('mobile apps development', 'mobilní aplikace'),
    ('mobile apps', 'mobilní aplikace'),
    ('gargamel', 'gargamel'),
])
def test_job_requirement(requirement, expected):
    assert template_filters.job_requirement(requirement) == expected


@pytest.mark.parametrize('type_,expected', [
    ('full-time', 'plný úvazek'),
    ('part-time', 'částečný úvazek'),
    ('paid-internship', 'placená stáž'),
    ('unpaid-internship', 'neplacená stáž'),
    ('volunteering', 'dobrovolnictví'),
    ('gargamel', 'gargamel'),
])
def test_job_type(type_, expected):
    assert template_filters.job_type(type_) == expected
