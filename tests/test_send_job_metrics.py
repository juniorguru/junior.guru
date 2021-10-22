from datetime import date
from pathlib import Path

import pytest
from jinja2 import Template
from playhouse.sqlite_ext import JSONField

from juniorguru.models import Job
from juniorguru.send.job_metrics import create_message
from testing_utils import prepare_job_data


class JobMock(Job):
    metrics = JSONField()


@pytest.fixture
def job_mock():
    data = prepare_job_data('123')
    data['metrics'] = dict(users=15, pageviews=25, applications=3)
    return JobMock(**data)


@pytest.fixture
def template():
    template_path = Path(__file__).parent.parent / 'juniorguru' / 'send' / 'templates' / 'job_metrics.html'
    return Template(template_path.read_text())


def test_create_message_metrics(job_mock, template):
    job_mock.metrics = dict(users=15, pageviews=25, applications=3)
    message = create_message(job_mock, template, date.today())
    html = message['html_content']

    assert '<b>15</b>' in html
    assert '<b>25</b>' in html


def test_create_message_start_end(job_mock, template):
    job_mock.posted_at = date(2020, 6, 1)
    job_mock.expires_at = date(2020, 7, 1)
    message = create_message(job_mock, template, date(2020, 6, 23))
    html = message['html_content']

    assert '22&nbsp;dní' in html
    assert 'schválen 1.6.2020' in html
    assert '8&nbsp;dní' in html
    assert 'vyprší 1.7.2020' in html


@pytest.mark.parametrize('expires_at,expected', [
    (date(2020, 7, 1), 'Jak se daří vašemu inzerátu? (Junior Software Engineer)'),
    (date(2020, 6, 25), 'Váš inzerát brzy vyprší! (Junior Software Engineer)'),
])
def test_create_message_subject(job_mock, template, expires_at, expected):
    job_mock.expires_at = expires_at
    message = create_message(job_mock, template, date(2020, 6, 20))

    assert message['subject'] == expected


def test_create_message_applications_zero(job_mock, template):
    job_mock.metrics = dict(users=15, pageviews=25, applications=0)
    message = create_message(job_mock, template, date(2020, 6, 23))
    html = message['html_content']

    assert 'uchazeč' not in html


def test_create_message_applications_non_zero(job_mock, template):
    job_mock.metrics = dict(users=15, pageviews=25, applications=5)
    message = create_message(job_mock, template, date(2020, 6, 23))
    html = message['html_content']

    assert 'uchazeč' in html
    assert '<b>5</b>' in html


def test_create_message_expires_soon(job_mock, template):
    job_mock.expires_at = date(2020, 7, 1)
    message = create_message(job_mock, template, date(2020, 6, 24))
    html = message['html_content']

    assert 'prodloužit o dalších 30&nbsp;dní' in html
    assert '1.199&nbsp;Kč' in html


def test_create_message_expires_not_soon(job_mock, template):
    job_mock.expires_at = date(2020, 7, 1)
    message = create_message(job_mock, template, date(2020, 6, 20))
    html = message['html_content']

    assert 'prodloužit o dalších 30&nbsp;dní' not in html
