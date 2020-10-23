from datetime import date
import os
import sys
import smtplib
import random

from juniorguru.lib.log import get_log
from juniorguru.send import job_metrics, logo_metrics


log = get_log('send')


EMAIL_BATCHES = (
    {'name': job_metrics.__name__,
     'generate_messages': job_metrics.generate_messages,
     'when': (lambda date: date.weekday() == 0),
     'when_text': 'Monday?'},
    {'name': logo_metrics.__name__,
     'generate_messages': logo_metrics.generate_messages,
     'when': (lambda date: date.today().day == 1),
     'when_text': 'First day of the month?'},
)


def main():
    config = os.environ
    debug = os.getenv('DEBUG', '--debug' in sys.argv)
    log.info(f"Debug: {'YES' if debug else 'NO'}")
    today = date.today()
    log.info(f"Today: {today:%Y-%m-%d}")

    for batch in EMAIL_BATCHES:
        log.info(f"About to send {batch['name']}")
        is_triggered = batch['when'](today)
        if is_triggered:
            log.error(f"{batch['when_text']} YES")
        else:
            log.error(f"{batch['when_text']} NO")
            if debug:
                log.info('Debug mode suppressed early exit')
            else:
                continue

        messages = list(batch['generate_messages'](today, debug=debug))
        log.info(f"The {batch['name']} generated {len(messages)} messages")

        if config.get('SMTP_ENABLED'):
            log.debug('Sending enabled')

            if debug:
                sample_message = random.choice(messages)
                log.info(f"Debug mode chose a message {sample_message!r}")
                messages = [sample_message]

            server = smtplib.SMTP(host=config['SMTP_HOST'],
                                port=int(config['SMTP_PORT']))
            server.starttls()
            server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
            try:
                for message in messages:
                    log.debug(f"Sending message {message!r}")
                    server.send_message(message)
                    log.info(f"Sent message {message!r}")
            finally:
                server.quit()
        else:
            log.warning('Sending not enabled')


if __name__ == '__main__':
    main()
