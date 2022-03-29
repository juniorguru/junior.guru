from datetime import date
from pathlib import Path

import pytest
from jinja2 import Template

from juniorguru.models import ListedJob, SubmittedJob
from juniorguru.sync.jobs_emails import debug_message, create_message, should_send


TEMPLATE_PATH = Path(__file__).parent.parent / 'juniorguru' / 'sync' / 'jobs_emails' / 'templates' / 'job_metrics.html'


@pytest.fixture
def job():
    return ListedJob(submitted_job=SubmittedJob())


@pytest.fixture
def template():
    return Template(TEMPLATE_PATH.read_text())


@pytest.mark.parametrize('today, last_run_on, expected', [
    pytest.param(date(2022, 3, 28), None, True, id='on Monday, for the first time'),
    pytest.param(date(2022, 3, 30), None, False, id='on random day, for the first time'),
    pytest.param(date(2022, 3, 30), date(2022, 3, 28), False, id='on random day, last run this Monday'),
    pytest.param(date(2022, 4, 3), date(2022, 3, 28), False, id='on random day, last run this Monday'),
    pytest.param(date(2022, 3, 28), date(2022, 3, 21), True, id='on Monday, last run on previous Monday'),
    pytest.param(date(2022, 3, 30), date(2022, 3, 21), True, id='on random day, last run on previous Monday'),
    pytest.param(date(2022, 3, 28), date(2022, 3, 23), True, id='on Monday, last run on previous random day'),
    pytest.param(date(2022, 3, 30), date(2022, 3, 23), True, id='on random day, last run on previous random day'),
    pytest.param(date(2022, 3, 28), date(2022, 3, 28), False, id='on Monday, already sent today'),
])
def test_should_send(today, last_run_on, expected):
    assert should_send(today, last_run_on) == expected


def test_debug_message():
    message = dict(from_email=('From', 'sender@example.com'),
                   to_emails=[('To 1', 'to1@example.com'),
                              ('To 2', 'to2@example.com')],
                   bcc_emails=[('Bcc 1', 'bcc1@example.com'),
                               ('Bcc 2', 'bcc2@example.com')],
                   subject='Subject',
                   html_content='HTML <b>content</b>')
    message = debug_message(message)

    assert message == dict(from_email=('From', 'sender@example.com'),
                           to_emails=[('To 1', 'honza@junior.guru'),
                                       ('To 2', 'honza@junior.guru')],
                           bcc_emails=[],
                           subject='[DEBUG] Subject',
                           html_content='HTML <b>content</b>')


def test_create_message_simple_analytics_url(job, template):
    today = date(2022, 1, 17)
    job.submitted_job.id = 123
    job.submitted_job.posted_on = date(2021, 12, 28)
    job.submitted_job.expires_on = date(2022, 1, 27)

    message = create_message(job, template, today)
    html = message['html_content']

    assert ('https://simpleanalytics.com/junior.guru'
            '?search=paths%3A123'
            '&start=2021-12-28'
            '&end=2022-01-17') in html


def test_create_message_start_end(job, template):
    job.submitted_job.posted_on = date(2020, 6, 1)
    job.submitted_job.expires_on = date(2020, 7, 1)

    message = create_message(job, template, date(2020, 6, 23))
    html = message['html_content']

    assert '22 dní' in html
    assert 'schválen 1.6.2020' in html
    assert '8 dní' in html
    assert 'vyprší 1.7.2020' in html


@pytest.mark.parametrize('expires_on, expected', [
    (date(2020, 7, 1), 'Jak se daří vašemu inzerátu? (Junior Software Engineer)'),
    (date(2020, 6, 25), 'Váš inzerát brzy vyprší! (Junior Software Engineer)'),
])
def test_create_message_subject(job, template, expires_on, expected):
    job.title = 'Junior Software Engineer'
    job.submitted_job.posted_on = date(2020, 6, 1)
    job.submitted_job.expires_on = expires_on

    message = create_message(job, template, date(2020, 6, 20))

    assert message['subject'] == expected


def test_create_message_expires_soon(job, template):
    job.submitted_job.posted_on = date(2020, 6, 1)
    job.submitted_job.expires_on = date(2020, 7, 1)

    message = create_message(job, template, date(2020, 6, 24))
    html = message['html_content']

    assert 'prodloužit o dalších 30 dní' in html
    assert '1.199 Kč' in html


def test_create_message_expires_not_soon(job, template):
    job.submitted_job.posted_on = date(2020, 6, 1)
    job.submitted_job.expires_on = date(2020, 7, 1)

    message = create_message(job, template, date(2020, 6, 20))
    html = message['html_content']

    assert 'prodloužit o dalších 30 dní' not in html
