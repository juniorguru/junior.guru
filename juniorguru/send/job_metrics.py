from pathlib import Path
from urllib.parse import quote_plus

from jinja2 import Template

from juniorguru.models import Job


def generate_messages(today):
    jobs = Job.juniorguru_listing()

    template_path = Path(__file__).parent / 'templates' / 'job_metrics.html'
    template = Template(template_path.read_text())

    return (create_message(job, template, today) for job in jobs)


def create_message(job, template, today):
    if job.expires_soon(today):
        subject = 'Váš inzerát brzy vyprší!'
    else:
        subject = 'Jak se daří vašemu inzerátu?'
    subject = f'{subject} ({job.title})'

    from_email = ('junior.guru', 'metrics@junior.guru')
    to_emails = [(job.company_name, job.email)]
    bcc_emails = [('junior.guru', 'honza@junior.guru')]
    content = template.render(**prepare_template_context(job, today))

    return dict(from_email=from_email, to_emails=to_emails,
                bcc_emails=bcc_emails, subject=subject, html_content=content)


def prepare_template_context(job, today):
    return dict(title=job.title,
                company_name=job.company_name,
                company_name_urlencoded=quote_plus(job.company_name),
                pricing_plan=job.pricing_plan,
                url=f'https://junior.guru/jobs/{job.id}/',
                url_jobs='https://junior.guru/jobs/',
                url_index='https://junior.guru/',
                url_logo='https://junior.guru/static/images/logo-email.png',
                metrics=job.metrics,
                start_at=job.posted_at,
                start_days=job.days_since_posted(today),
                end_at=job.expires_at,
                end_days=job.days_until_expires(today),
                expires_soon=job.expires_soon(today))
