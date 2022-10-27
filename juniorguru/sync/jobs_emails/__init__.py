import os
import random
import smtplib
from datetime import date, timedelta
from email.headerregistry import Address
from email.message import EmailMessage
from pathlib import Path
from pprint import pformat

import click
from jinja2 import Template

from juniorguru.lib import loggers
from juniorguru.cli.sync import Command
from juniorguru.models.job import ListedJob


JOBS_EMAILS_DEBUG = os.getenv('JOBS_EMAILS_DEBUG')

JOBS_EMAILS_LAST_RUN_FILE = Path('juniorguru/data/jobs-emails.txt')

JOBS_EMAILS_SENDING_ENABLED = bool(int(os.getenv('JOBS_EMAILS_SENDING_ENABLED', 0)))

SMTP_HOST = os.environ['SMTP_HOST'] if JOBS_EMAILS_SENDING_ENABLED else None

SMTP_PORT = os.environ['SMTP_PORT'] if JOBS_EMAILS_SENDING_ENABLED else None

SMTP_USERNAME = os.environ['SMTP_USERNAME'] if JOBS_EMAILS_SENDING_ENABLED else None

SMTP_PASSWORD = os.environ['SMTP_PASSWORD'] if JOBS_EMAILS_SENDING_ENABLED else None


logger = loggers.get(__name__)


@click.command(cls=Command, requires=['jobs-listing'])
def main():
    today = date.today()
    try:
        last_run_on = date.fromisoformat(JOBS_EMAILS_LAST_RUN_FILE.read_text().strip())
    except FileNotFoundError:
        last_run_on = None

    logger.info(f"{today:%A} {today}, " +
                (f"last run {last_run_on:%A} {last_run_on}, " if last_run_on else 'last run never, ') +
                f"debug {'YES' if JOBS_EMAILS_DEBUG else 'NO'}, " +
                f"sending enabled {'YES' if JOBS_EMAILS_SENDING_ENABLED else 'NO'}")

    if should_send(today, last_run_on):
        logger.info("Should send the emails, yay!")
    else:
        logger.info("Should NOT send the emails")
        if JOBS_EMAILS_DEBUG:
            logger.info('Debug mode suppressed early exit')
        else:
            return

    messages = list(generate_messages(today))
    logger.info(f"Generated {len(messages)} messages")
    for message_n, message in enumerate(messages, start=1):
        logger.debug(f'Message #{message_n}:\n' + pformat(message))

    if JOBS_EMAILS_SENDING_ENABLED:
        logger.debug('Sending enabled')
        if JOBS_EMAILS_DEBUG:
            sample_message = random.choice(messages)
            logger.info(f"Debug mode chose a message '{sample_message['subject']}'")
            messages = [debug_message(sample_message)]

        server = smtplib.SMTP(host=SMTP_HOST, port=int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        try:
            for message in messages:
                logger.debug(f"Sending message '{message['subject']}'")
                server.send_message(envelope(message))
                logger.info(f"Sent message '{message['subject']}'")
        finally:
            server.quit()

        logger.info(f"Writing to {JOBS_EMAILS_LAST_RUN_FILE}")
        JOBS_EMAILS_LAST_RUN_FILE.write_text(today.isoformat())
    else:
        logger.warning('Sending not enabled')


def should_send(today, last_run_on):
    if today.weekday() == 0:
        if last_run_on == today:
            return False
        return True
    if last_run_on:
        this_monday = today - timedelta(days=today.weekday())
        if last_run_on < this_monday:
            return True
    return False


def debug_message(message):
    return {**message, **dict(
        to_emails=[(name, 'honza@junior.guru') for
                    name, email_address in message['to_emails']],
        subject=f"[DEBUG] {message['subject']}",
        bcc_emails=[]
    )}


def envelope(message):
    em = EmailMessage()

    display_name, addr_spec = message['from_email']
    em['From'] = Address(display_name=display_name, addr_spec=addr_spec)

    em['To'] = [Address(display_name=display_name, addr_spec=addr_spec)
                for display_name, addr_spec in message['to_emails']]

    if message.get('bcc_emails'):
        em['Bcc'] = [Address(display_name=display_name, addr_spec=addr_spec)
                     for display_name, addr_spec in message['bcc_emails']]

    em['Subject'] = message['subject']
    em.add_header('Content-Type', 'text/html; charset="utf-8"')
    em.set_payload(message['html_content'].encode('utf-8'))
    return em


def generate_messages(today):
    jobs = ListedJob.submitted_listing()

    template_path = Path(__file__).parent / 'templates' / 'job_metrics.html'
    template = Template(template_path.read_text())

    return (create_message(job, template, today) for job in jobs)


def create_message(job, template, today):
    if job.submitted_job.expires_soon(today):
        subject = 'Váš inzerát brzy vyprší!'
    else:
        subject = 'Jak se daří vašemu inzerátu?'
    subject = f'{subject} ({job.title})'

    from_email = ('junior.guru', 'metrics@junior.guru')
    to_emails = [(job.company_name, job.apply_email)]
    bcc_emails = [('junior.guru', 'honza@junior.guru')]
    content = template.render(**prepare_template_context(job, today))

    return dict(from_email=from_email, to_emails=to_emails,
                bcc_emails=bcc_emails, subject=subject, html_content=content)


def prepare_template_context(job, today):
    return dict(title=job.title,
                company_name=job.company_name,
                url=f'https://junior.guru/jobs/{job.submitted_job.id}/',
                url_jobs='https://junior.guru/jobs/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                url_analytics=f'https://simpleanalytics.com/junior.guru?search=paths%3A{job.submitted_job.id}&start={job.submitted_job.posted_on}&end={today}',
                start_at=job.submitted_job.posted_on,
                start_days=job.submitted_job.days_since_posted(today),
                end_at=job.submitted_job.expires_on,
                end_days=job.submitted_job.days_until_expires(today),
                expires_soon=job.submitted_job.expires_soon(today))
