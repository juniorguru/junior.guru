import os
import random
import sys
from datetime import date
from pathlib import Path
from pprint import pformat
from urllib.parse import quote_plus

from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, From, Mail, To

from juniorguru.log import get_log
from juniorguru.models import Logo


DEBUG = os.getenv('DEBUG_SEND_LOGO_METRICS', '--debug' in sys.argv)
SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


log = get_log(__name__)


def main():
    logos = Logo.listing()
    log.info(f'Debug? {DEBUG}')
    if DEBUG and SENDGRID_ENABLED:
        logos = [random.choice(logos)]
        log.info(f'Debug mode chose the following logo: {logos[0]}')

    # is_monday = date.today().weekday() == 0
    # log.info(f'Monday? {is_monday}')
    # if not is_monday:
    #     log.error('Not Monday')
    #     if DEBUG:
    #         log.info('Debug mode suppressed early exit')
    #     else:
    #         sys.exit(0)

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
    sys.exit(status)



def create_message(logo, template, today=None):
    if logo.expires_soon(today):
        subject = 'Vaše sponzorství příručky brzy vyprší!'
    else:
        subject = 'Jak se daří příručce?'
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
    return {}
    # return dict(title=job.title,
    #             company_name=job.company_name,
    #             company_name_urlencoded=quote_plus(job.company_name),
    #             pricing_plan=job.pricing_plan,
    #             url=f'https://junior.guru/jobs/{job.id}/',
    #             url_jobs='https://junior.guru/jobs/',
    #             url_index='https://junior.guru/',
    #             url_logo='https://junior.guru/static/images/logo-email.png',
    #             metrics=job.metrics,
    #             start_at=job.approved_at,
    #             start_days=job.days_since_approved(today),
    #             end_at=job.expires_at,
    #             end_days=job.days_until_expires(today),
    #             expires_soon=job.expires_soon(today),
    #             newsletter_mentions=job.newsletter_mentions,
    #             newsletter_archive_url='https://us3.campaign-archive.com/home/?u=7d3f89ef9b2ed953ddf4ff5f6&id=e231b1fb75')


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
    main()
