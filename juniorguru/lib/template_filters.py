import math
import random
import re
from datetime import date, datetime
from operator import itemgetter
from urllib.parse import unquote, urljoin

import arrow
from slugify import slugify
from markupsafe import Markup

from juniorguru.lib.md import md as md_


def email_link(email):
    user, server = email.split('@')
    return Markup(
        f'<a href="mailto:{user}&#64;{server}">'
        f'{user}&#64;<!---->{server}'
        '</a>'
    )


def relative_url(url):
    return url.replace('https://junior.guru', '')


def absolute_url(url):
    return urljoin('https://junior.guru', url)


def md(*args, **kwargs):
    return Markup(md_(*args, **kwargs))


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


def tag_label(tag):
    return TAGS_MAPPING[tag]


def to_datetime(dt_str):
    return datetime.fromisoformat(dt_str)


def local_time(dt):
    return arrow.get(dt).to('Europe/Prague').format('H:mm')


def weekday(dt):
    return ['neděle', 'pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota'][int(dt.strftime('%w'))]


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


def metric(value):
    # https://realpython.com/python-rounding/
    decimals = len(str(int(value))) - 2
    multiplier = 10 ** decimals
    number = int(math.floor((value / multiplier) + 0.5) * multiplier)
    return thousands(str(number))


def thousands(value):
    return re.sub(r'(\d)(\d{3})$', r'\1.\2', str(value))


def sample(items, n=2, sample_fn=None):
    items = list(items)
    if len(items) <= n:
        return items
    return (sample_fn or random.sample)(items, n)


def sample_jobs(jobs, n=2, sample_fn=None):
    jobs = list(jobs)
    if len(jobs) <= n:
        return jobs
    preferred_jobs = [job for job in jobs if job.is_submitted]
    if len(preferred_jobs) >= n:
        jobs = preferred_jobs
    return (sample_fn or random.sample)(jobs, n)


def icon(name, classes=None, alt=None):
    if classes:
        classes = set(filter(None, [cls.strip() for cls in classes.split(' ')]))
    else:
        classes = set()
    classes.add('bi')
    classes.add(f'bi-{name}')
    class_list = ' '.join(sorted(classes))

    alt = f' role="img" aria-label="{alt}"' if alt else ''
    return Markup(f'<i class="{class_list}"{alt}></i>')


def docs_url(files, src_path):
    for file in files:
        if file.src_path == src_path:
            return file.url
    src_paths = ', '.join([f.src_path for f in files])
    raise ValueError(f"Could not find '{src_path}' in given MkDocs files: {src_paths}")


REVENUE_CATEGORIES = {
    'donations': 'dobrovolné příspěvky',
    'jobs': 'inzerce nabídek práce',
    'memberships': 'individuální členství',
    'partnerships': 'firemní členství',
}


def revenue_categories(breakdown_mapping):
    return sorted((
        (REVENUE_CATEGORIES[name], value) for name, value
        in breakdown_mapping.items()
    ), key=itemgetter(1), reverse=True)


def money_breakdown_ptc(breakdown_mapping):
    items = list(breakdown_mapping.items())
    total = sum(item[1] for item in items)
    return {item[0]: math.ceil(item[1] * 100 / total) for item in items}


class TemplateError(Exception):
    pass


def assert_empty(collection):
    if len(collection):
        raise TemplateError(f"{type(collection).__name__} not empty: {', '.join(collection)}")
    return ''


def screenshot_url(url):
    slug = slugify(unquote(url)) \
        .removeprefix('http-') \
        .removeprefix('https-') \
        .removeprefix('www-')
    return f'static/images/screenshots/{slug}.jpg'
