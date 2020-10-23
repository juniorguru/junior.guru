from pathlib import Path

from jinja2 import Template

from juniorguru.models import Logo


def generate_messages(today):
    logos = Logo.listing()

    template_path = Path(__file__).parent / 'templates' / 'logo_metrics.html'
    template = Template(template_path.read_text())

    return (create_message(logo, template, today) for logo in logos)


def create_message(logo, template, today):
    if logo.expires_soon(today):
        subject = 'Vaše sponzorství příručky brzy vyprší!'
    else:
        subject = 'Jak se daří vašemu logu na příručce?'
    subject = f'{subject} ({logo.name})'

    from_email = ('junior.guru', 'metrics@junior.guru')
    to_emails = [(logo.name, logo.email)]
    bcc_emails = [('junior.guru', 'ahoj@junior.guru')]
    content = template.render(**prepare_template_context(logo, today))

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
