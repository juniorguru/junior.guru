from pathlib import Path
from datetime import datetime

from jinja2 import Markup
from markdown import markdown
from markdown.extensions.toc import TocExtension

from . import app


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


TYPES_MAPPING = {
    'full-time': 'plný úvazek',
    'part-time': 'částečný úvazek',
    'paid-internship': 'placená stáž',
    'unpaid-internship': 'neplacená stáž',
    'volunteering': 'dobrovolnictví',
}


@app.template_filter()
def job_type(type_):
    try:
        return TYPES_MAPPING[type_]
    except KeyError:
        return type_


@app.template_filter()
def ago(dt, now=None):
    now = now or datetime.now()
    days = (now - dt).days
    try:
        return ('dnes', 'včera', 'předevčírem')[days]
    except IndexError:
        return f'před {days} dny'
