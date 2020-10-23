from pathlib import Path

from jinja2 import Template

from juniorguru.lib.emails import create_message
from juniorguru.models import Logo


def generate_messages(today, debug=False):
    logos = Logo.listing()

    template_path = Path(__file__).parent / 'templates' / 'logo_metrics.html'
    template = Template(template_path.read_text())

    for logo in logos:
        message_data = prepare_message_data(logo, template, today, debug=debug)
        yield create_message(**message_data)


def prepare_message_data(logo, template, today, debug=False):
    if logo.expires_soon(today):
        subject = 'Vaše sponzorství příručky brzy vyprší!'
    else:
        subject = 'Jak se daří vašemu logu na příručce?'
    subject = f'{subject} ({logo.name})'

    from_email = ('junior.guru', 'metrics@junior.guru')
    bcc_emails = []
    content = template.render(**prepare_template_context(logo, today))

    if debug:
        to_emails = [(logo.name, 'ahoj@junior.guru')]
        subject = f'[DEBUG] {subject}'
    else:
        to_emails = [(logo.name, logo.email)]
        bcc_emails = [('junior.guru', 'ahoj@junior.guru')]

    return dict(from_email=from_email, to_emails=to_emails,
                bcc_emails=bcc_emails, subject=subject, html_content=content)


def prepare_template_context(logo, today):
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
