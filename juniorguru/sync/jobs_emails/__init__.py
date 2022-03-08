import os
from datetime import date
from pathlib import Path
import smtplib
import random
from email.message import EmailMessage
from email.headerregistry import Address

from jinja2 import Template

from juniorguru.lib import loggers
from juniorguru.lib.tasks import sync_task
from juniorguru.models import ListedJob


logger = loggers.get(__name__)


@sync_task()
def main():
    config = os.environ
    debug = os.getenv('DEBUG_SEND')
    logger.info(f"Debug: {'YES' if debug else 'NO'}")
    today = date.today()
    logger.info(f"Today: {today:%Y-%m-%d}")
    logger.info(f"About to send {__name__}")
    if today.weekday() == 0:
        logger.error('Monday? YES')
    else:
        logger.error('Monday? NO')
        if debug:
            logger.info('Debug mode suppressed early exit')
        else:
            return

    messages = list(generate_messages(today))
    logger.info(f"The {__name__} generated {len(messages)} messages")

    if config.get('SMTP_ENABLED'):
        logger.debug('Sending enabled')

        if debug:
            sample_message = random.choice(messages)
            logger.info(f"Debug mode chose a message '{sample_message['subject']}'")
            messages = [debug_message(sample_message)]

        server = smtplib.SMTP(host=config['SMTP_HOST'],
                                port=int(config['SMTP_PORT']))
        server.starttls()
        server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
        try:
            for message in messages:
                logger.debug(f"Sending message '{message['subject']}'")
                server.send_message(envelope(message))
                logger.info(f"Sent message '{message['subject']}'")
        finally:
            server.quit()
    else:
        logger.warning('Sending not enabled')


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
                url=f'https://junior.guru/jobs/{job.id}/',
                url_jobs='https://junior.guru/jobs/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                url_analytics=f'https://simpleanalytics.com/junior.guru?search=paths%3A{job.id}&start={job.posted_at}&end={today}',
                start_at=job.submitted_job.posted_at,
                start_days=job.submitted_job.days_since_posted(today),
                end_at=job.submitted_job.expires_at,
                end_days=job.submitted_job.days_until_expires(today),
                expires_soon=job.submitted_job.expires_soon(today))
