import json
import logging
import os
from pprint import pformat

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, Mail, To

from juniorguru.log import get_log
from juniorguru.models import Job


SENDGRID_ENABLED = os.getenv('SENDGRID_ENABLED')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')


log = get_log(__name__)


def main():
    message = Mail(from_email=From('metrics@junior.guru', 'junior.guru'),
                   to_emails=To('mail@honzajavorek.cz', 'Honza Javorek'),
                   subject='Sending with Twilio SendGrid is Fun',
                   plain_text_content='and easy to do anywhere, even with Python',
                   html_content='<strong>and easy to do anywhere, even with Python</strong>')
    send(message)


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
