from datetime import datetime
from pathlib import Path

import arrow
from jinja2 import Markup
from markdown import markdown
from markdown.extensions.toc import TocExtension

from juniorguru.web import app


@app.template_filter()
def email_link(email):
    user, server = email.split('@')
    return Markup(
        f'<a href="mailto:{user}&#64;{server}">'
        f'{user}&#64;<!---->{server}'
        '</a>'
    )


@app.template_filter()
def md(markdown_text, heading_level_base=1):
    toc = TocExtension(marker='', baselevel=heading_level_base)
    markup = markdown(markdown_text, output_format='html5', extensions=[toc])
    return Markup(markup)


REQUIREMENTS_MAPPING = {
    'mainstream programming language': 'základy programování',
    'databases': 'databáze',
    'data analysis': 'datová analýza',
    'servers and operations': 'správa serverů',
    'Linux and command line': 'Linux a příkazová řádka',
    'Linux': 'Linux a příkazová řádka',
    'web backend': 'webový backend',
    'web frontend': 'webový frontend',
    'mobile apps development': 'mobilní aplikace',
    'mobile apps': 'mobilní aplikace',
}


@app.template_filter()
def job_requirement(requirement):
    try:
        return REQUIREMENTS_MAPPING[requirement]
    except KeyError:
        return requirement


EMPLOYMENT_TYPES_MAPPING = {
    'full-time': 'plný úvazek',
    'part-time': 'částečný úvazek',
    'contract': 'kontrakt',
    'paid internship': 'placená stáž',
    'unpaid internship': 'neplacená stáž',
    'internship': 'stáž',
    'volunteering': 'dobrovolnictví',
}


@app.template_filter()
def employment_type(type_):
    try:
        return EMPLOYMENT_TYPES_MAPPING[type_]
    except KeyError:
        return type_


@app.template_filter()
def employment_types(types, sep=', '):
    if not types:
        raise ValueError('Employment types must not be empty')
    return sep.join(employment_type(type_) for type_ in types)


@app.template_filter()
def to_datetime(dt_str):
    return datetime.fromisoformat(dt_str)


@app.template_filter()
def ago(dt, now=None):
    dt = dt if dt.tzinfo else arrow.get(dt, 'UTC')
    now = now or datetime.utcnow()
    now = now if now.tzinfo else arrow.get(now, 'UTC')
    days = (now - dt).days
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
