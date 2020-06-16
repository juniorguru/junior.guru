import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from pprint import pformat

from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, To

from juniorguru.log import get_log
from juniorguru.models import GlobalMetric, Job


SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_LIMIT = 100


log = get_log(__name__)


def main():
    jobs = Job.juniorguru_listing()
    jobs_count = len(jobs)

    log.info(f'Jobs: {jobs_count}')
    if jobs_count > SENDGRID_LIMIT:
        log.error(f'Jobs count is too high! {jobs_count} > {SENDGRID_LIMIT}')

    template_path = Path(__file__).parent / 'templates' / 'metrics.html'
    template = Template(template_path.read_text())

    global_metrics = GlobalMetric.as_dict()
    for job in jobs:
        send(create_message(job, global_metrics, template))


def create_message(job, global_metrics, template):
    from_email = From('metrics@junior.guru', 'junior.guru')
    to_email = To('mail@honzajavorek.cz', job.company_name)  # TODO job.email
    subject = f'Jak se daří vašemu inzerátu? ({job.title})'
    content = template.render(**create_template_context(job, global_metrics))

    return Mail(from_email=from_email, to_emails=to_email,
                subject=subject, html_content=content)


def create_template_context(job, global_metrics, today=None):
    today = today or date.today()
    starts_at = job.effective_approved_at
    start_days = (today - starts_at).days
    ends_at = job.expires_at or (today + timedelta(days=30))
    end_days = (ends_at - today).days

    metrics_days = start_days - 1  # the per job data is up to yesterday
    metrics = calc_metrics(metrics_days, job.metrics, global_metrics)

    return dict(title=job.title,
                company_name=job.company_name,
                url=f'https://junior.guru/jobs/{job.id}/',
                url_jobs='https://junior.guru/jobs/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                metrics=metrics,
                starts_at=starts_at,
                start_days=start_days,
                ends_at=ends_at,
                end_days=end_days,
                newsletter_at=job.newsletter_at,
                newsletter_url='https://us3.campaign-archive.com/home/?u=7d3f89ef9b2ed953ddf4ff5f6&id=e231b1fb75')


def calc_metrics(days, job_metrics, global_metrics):
    avg_users = days * global_metrics['avg_daily_users_per_job']
    users_performance = (100 * job_metrics['users']) / avg_users

    avg_pageviews = days * global_metrics['avg_daily_pageviews_per_job']
    pageviews_performance = (100 * job_metrics['pageviews']) / avg_pageviews

    avg_applications = days * global_metrics['avg_daily_applications_per_job']
    applications_performance = (100 * job_metrics['applications']) / avg_applications

    return dict(job_metrics,
                avg_users=avg_users,
                users_performance=users_performance,
                avg_pageviews=avg_pageviews,
                pageviews_performance=pageviews_performance,
                avg_applications=avg_applications,
                applications_performance=applications_performance)


def send(message):
    status = 0
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
            status = 1
    else:
        log.warning('SendGrid not enabled')
    sys.exit(status)


if __name__ == '__main__':
    main()
