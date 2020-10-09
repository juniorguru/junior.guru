import re
import math
import random
from datetime import date, datetime

from jinja2 import Markup

from juniorguru.web import app
from juniorguru.lib.md import md as md_


@app.template_filter()
def email_link(email):
    user, server = email.split('@')
    return Markup(
        f'<a href="mailto:{user}&#64;{server}">'
        f'{user}&#64;<!---->{server}'
        '</a>'
    )


@app.template_filter()
def md(*args, **kwargs):
    return Markup(md_(*args, **kwargs))


@app.template_filter()
def remove_p(html):
    return Markup(re.sub(r'</?p[^>]*>', '', html))


TAGS_MAPPING = {
    'NEW': 'nové',
    'REMOTE': 'na dálku',
    'PART_TIME': 'částečný úvazek',
    'CONTRACT': 'kontrakt',
    'INTERNSHIP': 'stáž',
    'UNPAID_INTERNSHIP': 'neplacená stáž',
    'VOLUNTEERING': 'dobrovolnictví',
    'ALSO_PART_TIME': 'lze i částečný úvazek',
    'ALSO_CONTRACT': 'lze i kontrakt',
    'ALSO_INTERNSHIP': 'lze i stáž',
}


@app.template_filter()
def tag_label(tag):
    return TAGS_MAPPING[tag]


@app.template_filter()
def to_datetime(dt_str):
    return datetime.fromisoformat(dt_str)


@app.template_filter()
def ago(value, now=None):
    today = now.date() if now else date.today()
    try:
        value = value.date()
    except AttributeError:
        pass
    days = (today - value).days
    try:
        return ('dnes', 'včera', 'předevčírem')[days]
    except IndexError:
        return f'před {days} dny'


@app.template_filter()
def sections(sections):
    def yaml_str(s):
        return f'"{s}"' if ':' in s else s

    yaml = ''
    for section in sections:
        if section.get('heading'):
            yaml += ('\n'
                    f"- heading: {yaml_str(section['heading'])}\n"
                    f"  type: {section['type']}\n")
        else:
            yaml += f"\n- type: {section['type']}\n"
        yaml += '  contents:\n'
        for item in section['contents']:
            yaml += f'    - {yaml_str(item)}\n'
    return yaml.strip()


@app.template_filter()
def metric(value):
    # https://realpython.com/python-rounding/
    decimals = len(str(int(value))) - 2
    multiplier = 10 ** decimals
    number = int(math.floor((value / multiplier) + 0.5) * multiplier)
    return re.sub(r'000$', 'tis', str(number))


@app.template_filter()
def sample_jobs(jobs, n=2, sample_fn=None):
    jobs = list(jobs)
    if len(jobs) <= n:
        return jobs
    preferred_jobs = [job for job in jobs if job.source == 'juniorguru']
    if len(preferred_jobs) >= n:
        jobs = preferred_jobs
    return (sample_fn or random.sample)(jobs, n)
