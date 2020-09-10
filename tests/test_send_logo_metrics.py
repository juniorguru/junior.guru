from datetime import date
from pathlib import Path

import pytest
from jinja2 import Template
from playhouse.sqlite_ext import JSONField

from juniorguru.models import Logo
from juniorguru.send.logo_metrics import create_message
from testing_utils import prepare_logo_data


class LogoMock(Logo):
    metrics = JSONField()


@pytest.fixture
def logo_mock():
    data = prepare_logo_data('123')
    data['metrics'] = dict(users=15, pageviews=25, clicks=3)
    return LogoMock(**data)


@pytest.fixture
def template():
    template_path = Path(__file__).parent.parent / 'juniorguru' / 'send' / 'templates' / 'logo_metrics.html'
    return Template(template_path.read_text())


def test_create_message_metrics(logo_mock, template):
    logo_mock.metrics = dict(users=15, pageviews=25, clicks=3)
    message = create_message(logo_mock, template)
    html = message.get()['content'][0]['value']

    assert '<b>15</b>' in html
    assert '<b>25</b>' in html


def test_create_message_start_end(logo_mock, template):
    logo_mock.starts_at = date(2020, 6, 1)
    logo_mock.expires_at = date(2020, 7, 1)
    message = create_message(logo_mock, template, today=date(2020, 6, 23))
    html = message.get()['content'][0]['value']

    assert '22&nbsp;dní' in html
    assert 'logo zobrazeno od&nbsp;1.6.2020' in html
    assert '8&nbsp;dní' in html
    assert 'sponzorství vyprší 1.7.2020' in html


@pytest.mark.parametrize('expires_at,expected', [
    (date(2020, 10, 1), 'Jak se daří vašemu logu na příručce? (Awesome Company)'),
    (date(2020, 6, 25), 'Vaše sponzorství příručky brzy vyprší! (Awesome Company)'),
])
def test_create_message_subject(logo_mock, template, expires_at, expected):
    logo_mock.expires_at = expires_at
    message = create_message(logo_mock, template, today=date(2020, 6, 20))

    assert message.get()['subject'] == expected


def test_create_message_job_slots_zero(logo_mock, template):
    logo_mock.job_slots = 0
    message = create_message(logo_mock, template, today=date(2020, 6, 23))
    html = message.get()['content'][0]['value']

    assert 'paušál' not in html
    assert 'inzerát' not in html


def test_create_message_job_slots_non_zero(logo_mock, template):
    logo_mock.job_slots = 43
    message = create_message(logo_mock, template, today=date(2020, 6, 23))
    html = message.get()['content'][0]['value']

    assert 'paušál' in html
    assert 'současně inzerátů' in html
    assert '<b>43</b>' in html


def test_create_message_clicks_zero(logo_mock, template):
    logo_mock.metrics = dict(users=15, pageviews=25, clicks=0)
    message = create_message(logo_mock, template, today=date(2020, 6, 23))
    html = message.get()['content'][0]['value']

    assert 'kliknutí' not in html


def test_create_message_clicks_non_zero(logo_mock, template):
    logo_mock.metrics = dict(users=15, pageviews=25, clicks=5)
    message = create_message(logo_mock, template, today=date(2020, 6, 23))
    html = message.get()['content'][0]['value']

    assert 'kliknutí' in html
    assert '<b>5</b>' in html


def test_create_message_expires_soon(logo_mock, template):
    logo_mock.expires_at = date(2020, 7, 1)
    message = create_message(logo_mock, template, today=date(2020, 6, 24))
    html = message.get()['content'][0]['value']

    assert 'Prodlužte' in html
    assert 'https://junior.guru/hire-juniors/#handbook' in html


def test_create_message_expires_not_soon(logo_mock, template):
    logo_mock.expires_at = date(2020, 7, 1)
    message = create_message(logo_mock, template, today=date(2020, 4, 20))
    html = message.get()['content'][0]['value']

    assert 'Prodlužte' not in html
