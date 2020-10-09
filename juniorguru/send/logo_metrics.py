import os
import random
import sys
from pathlib import Path
from pprint import pformat
from datetime import date

from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, From, Mail, To

from juniorguru.lib.log import get_log
from juniorguru.models import Logo


DEBUG = os.getenv('DEBUG_SEND_LOGO_METRICS', '--debug' in sys.argv)
SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


log = get_log('logo_metrics')


def main():
    logos = Logo.listing()
    log.info(f'Debug? {DEBUG}')
    if DEBUG and SENDGRID_ENABLED:
        logos = [random.choice(logos)]
        log.info(f'Debug mode chose the following logo: {logos[0]}')

    is_first_day_of_month = date.today().day == 1
    log.info(f'First day of the month? {is_first_day_of_month}')
    if not is_first_day_of_month:
        log.error('Not first day of the month')
        if DEBUG:
            log.info('Debug mode suppressed early exit')
        else:
            return 0

    logos_count = len(logos)
    log.info(f'Logos: {logos_count}')

    template_path = Path(__file__).parent / 'templates' / 'logo_metrics.html'
    template = Template(template_path.read_text())

    status = 0
    for logo in logos:
        try:
            message = create_message(logo, template)
            log.info('Sending\n' + pformat(message.get()))
            send(message)
        except Exception as e:
            log.exception(f'SendGrid error: {e}')
            status = 1
    return status


def create_message(logo, template, today=None):
    if logo.expires_soon(today):
        subject = 'Vaše sponzorství příručky brzy vyprší!'
    else:
        subject = 'Jak se daří vašemu logu na příručce?'
    subject = f'{subject} ({logo.name})'

    from_email = From('metrics@junior.guru', 'junior.guru')
    content = template.render(**create_template_context(logo, today))

    if DEBUG:
        to_emails = [To('ahoj@junior.guru', logo.name)]
        subject = f'[DEBUG] {subject}'
    else:
        to_emails = [To(logo.email, logo.name),
                     Bcc('ahoj@junior.guru', 'junior.guru')]

    return Mail(from_email=from_email, to_emails=to_emails,
                subject=subject, html_content=content)


def create_template_context(logo, today=None):
    return dict(name=logo.name,
                months=logo.months,
                job_slots=logo.job_slots,
                url=logo.link,
                url_jobs='https://junior.guru/jobs/',
                url_handbook='https://junior.guru/candidate-handbook/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                metrics=logo.metrics,
                start_at=logo.starts_at,
                start_days=logo.days_since_started(today),
                end_at=logo.expires_at,
                end_days=logo.days_until_expires(today),
                expires_soon=logo.expires_soon(today))


def send(message):
    if SENDGRID_ENABLED:
        response = SendGridAPIClient(SENDGRID_API_KEY).send(message)
        response_info = dict(status_code=response.status_code,
                             body=response.body,
                             headers=dict(response.headers.items()))
        log.debug('SendGrid response\n' + pformat(response_info))
    else:
        log.warning('SendGrid not enabled')


if __name__ == '__main__':
    sys.exit(main())
