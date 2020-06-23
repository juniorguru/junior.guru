import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from pprint import pformat
from urllib.parse import quote_plus

from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Bcc, From, Mail, To

from juniorguru.log import get_log
from juniorguru.models import GlobalMetric, Job


IS_MONDAY = bool(os.getenv('IS_MONDAY', date.today().weekday() == 0))
SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_LIMIT = 100


log = get_log(__name__)


def main():
    jobs = Job.juniorguru_listing()
    jobs_count = len(jobs)

    log.info(f'Monday? {IS_MONDAY}')
    if not IS_MONDAY:
        log.error(f'Not Monday')
        sys.exit(0)

    log.info(f'Jobs: {jobs_count}')
    if jobs_count > SENDGRID_LIMIT:
        log.error(f'Jobs count is too high! {jobs_count} > {SENDGRID_LIMIT}')

    template_path = Path(__file__).parent / 'templates' / 'metrics.html'
    template = Template(template_path.read_text())

    status = 0
    global_metrics = GlobalMetric.as_dict()
    for job in jobs:
        try:
            message = create_message(job, global_metrics, template)
            log.info('Sending\n' + pformat(message.get()))
            send(message)
        except Exception as e:
            log.exception(f'SendGrid error: {e}')
            status = 1
    sys.exit(status)



def create_message(job, global_metrics, template):
    from_email = From('metrics@junior.guru', 'junior.guru')
    to_email = To(job.email, job.company_name)
    to_bcc_email = Bcc('ahoj@junior.guru', 'junior.guru')
    subject = f'Jak se daří vašemu inzerátu? ({job.title})'
    content = template.render(**create_template_context(job, global_metrics))

    return Mail(from_email=from_email, to_emails=[to_email, to_bcc_email],
                subject=subject, html_content=content)


def create_template_context(job, global_metrics, today=None):
    today = today or date.today()
    starts_at = job.effective_approved_at
    start_days = (today - starts_at).days
    ends_at = job.expires_at or (today + timedelta(days=30))
    end_days = (ends_at - today).days

    return dict(title=job.title,
                company_name=job.company_name,
                company_name_urlencoded=quote_plus(job.company_name),
                url=f'https://junior.guru/jobs/{job.id}/',
                url_jobs='https://junior.guru/jobs/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                metrics=job.metrics,
                starts_at=starts_at,
                start_days=start_days,
                ends_at=ends_at,
                end_days=end_days,
                show_applications_note=(job.metrics['applications'] > 0
                                        and starts_at < date(2020, 5, 15)),
                newsletter_at=job.newsletter_at,
                newsletter_url='https://us3.campaign-archive.com/home/?u=7d3f89ef9b2ed953ddf4ff5f6&id=e231b1fb75')


def send(message):
    if SENDGRID_ENABLED:
        response = SendGridAPIClient(SENDGRID_API_KEY).send(message)
        response_info = dict(status_code=response.status_code,
                             body=response.body,
                             headers=dict(response.headers.items()))
        log.debug(f'SendGrid response\n' + pformat(response_info))
    else:
        log.warning('SendGrid not enabled')


if __name__ == '__main__':
    main()
