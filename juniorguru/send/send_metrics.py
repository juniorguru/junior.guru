import json
import logging
import os
from datetime import date, timedelta
from pprint import pformat
from textwrap import dedent

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

    for job in jobs:
        send(create_message(today, job))


def create_message(today, job):
    from_email = From('metrics@junior.guru', 'junior.guru')
    to_email = To('mail@honzajavorek.cz', job.company_name)  # TODO job.email

    starts_at = job.effective_approved_at
    start_days = (today - starts_at).days
    ends_at = job.expires_at or (today + timedelta(days=30))
    end_days = (ends_at - today).days

    archive_url = 'https://us3.campaign-archive.com/home/?u=7d3f89ef9b2ed953ddf4ff5f6&id=e231b1fb75'
    if job.newsletter_at:
        newsletter = f'ano (odeslán {job.newsletter_at.day}.{job.newsletter_at.month}.{job.newsletter_at.year}, archiv: {archive_url})'
    else:
        newsletter = f'zatím ne (archiv: {archive_url})'

    subject = f'Jak se daří vašemu inzerátu? ({job.title})'
    content = dedent(f'''
        Hezký den!

        Tento pravidelný, automatický e-mail vám přišel, protože máte inzerát
        na stránce https://junior.guru/jobs/, a to konkrétně tento:

        Pozice: {job.title}
        Firma: {job.company_name}
        Odkaz: https://junior.guru/jobs/{job.id}/

        Jak se mu zatím daří?

        Trvání: {start_days} dní (inzerát schválen {starts_at.day}.{starts_at.month}.{starts_at.year})
        Zbývá: {end_days} dní (inzerát vyprší {ends_at.day}.{ends_at.month}.{ends_at.year})
        Byl inzerát v newsletteru? {newsletter}
        Počet návštěvníků: {job.metrics['users']}
        Počet zobrazení: {job.metrics['pageviews']}
        Počet uchazečů (klik na tlačítko): {job.metrics['applications']}

        Upozornění: Statistiky jsou podhodnocené a pouze orientační. Čísla
        pocházejí z nástroje Google Analytics, který mohou internetové
        prohlížeče blokovat. Počet uchazečů je měřen teprve od května 2020.

        Chcete-li inzerát změnit, zrušit, prodloužit, nebo máte-li jakýkoliv
        dotaz, jednoduše odpovězte na tento e-mail.

        Honza Javorek
        https://junior.guru/
    ''')

    # TODO html_content
    return Mail(from_email=from_email, to_emails=to_email, subject=subject,
                plain_text_content=content)


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
