import re
import math
from datetime import datetime

import arrow
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


EMPLOYMENT_TYPES_FOLDING = {
    'paid internship': ('internship', 'unpaid internship'),
    'internship': ('unpaid internship',),
    'contract': ('volunteering',),
    'part-time': ('volunteering',),
    'full-time': ('volunteering',),
}


@app.template_filter()
def employment_types(types, sep=', '):
    if not types:
        raise ValueError('Employment types must not be empty')

    types = list(types)
    for type_, folded_types in EMPLOYMENT_TYPES_FOLDING.items():
        if type_ in types:
            for folded_type in folded_types:
                try:
                    types.remove(folded_type)
                except ValueError:
                    pass

    return sep.join(employment_type(type_) for type_ in types) \
        .replace('plný úvazek, částečný', 'plný i částečný') \
        .replace('částečný úvazek, plný', 'plný i částečný')


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


@app.template_filter()
def metric(value):
    # https://realpython.com/python-rounding/
    decimals = len(str(int(value))) - 2
    multiplier = 10 ** decimals
    return int(math.floor((value / multiplier) + 0.5) * multiplier)
