import json
import os
from datetime import date, timedelta
from pathlib import Path
from pprint import pformat

from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, To

from juniorguru.log import get_log
from juniorguru.models import Job


SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_LIMIT = 100


log = get_log(__name__)


def main():
    today = date.today()
    jobs = Job.juniorguru_listing(today=today)
    jobs_count = len(jobs)

    log.info(f'Jobs: {jobs_count}')
    if jobs_count > SENDGRID_LIMIT:
        log.error(f'Jobs count is too high! {jobs_count} > {SENDGRID_LIMIT}')

    template_path = Path(__file__).parent / 'templates' / 'metrics.html'
    template = Template(template_path.read_text())

    for job in jobs[:2]:
        send(create_message(today, job, template))


def create_message(today, job, template):
    from_email = From('metrics@junior.guru', 'junior.guru')
    to_email = To('mail@honzajavorek.cz', job.company_name)  # TODO job.email
    subject = f'Jak se daří vašemu inzerátu? ({job.title})'

    starts_at = job.effective_approved_at
    ends_at = job.expires_at or (today + timedelta(days=30))
    content = template.render(title=job.title,
                              company_name=job.company_name,
                              url=f'https://junior.guru/jobs/{job.id}/',
                              metrics=job.metrics,
                              starts_at=starts_at,
                              start_days=(today - starts_at).days,
                              ends_at=ends_at,
                              ends_days=(ends_at - today).days,
                              newsletter_at=job.newsletter_at,
                              newsletter_url='https://us3.campaign-archive.com/home/?u=7d3f89ef9b2ed953ddf4ff5f6&id=e231b1fb75')

    return Mail(from_email=from_email, to_emails=to_email,
                subject=subject, html_content=content)


def send(message):
    log.info('Sending\n' + pformat(message.get()))
    if SENDGRID_ENABLED:
        try:
            response = SendGridAPIClient(SENDGRID_API_KEY).send(message)
            response_info = dict(status_code=response.status_code,
                                 body=response.body,
                                 headers=dict(response.headers.items()))
            log.debug(f'SendGrid response\n' + pformat(response_info))
        except Exception as e:
            log.exception(f'SendGrid error: {e}')
    else:
        log.warning('SendGrid not enabled')


if __name__ == '__main__':
    main()
