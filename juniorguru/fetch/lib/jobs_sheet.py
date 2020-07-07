import hashlib
import re
from datetime import timedelta, datetime
from urllib.parse import urlparse

import arrow


def coerce_record(record):
    return coerce({
        r'^timestamp$': ('posted_at', coerce_datetime),
        r'^company name$': ('company_name', coerce_text),
        r'^employment type$': ('employment_types', coerce_set),
        r'^job title$': ('title', coerce_text),
        r'^company website link$': ('company_link', coerce_text),
        r'^email address$': ('email', coerce_text),
        r'^job location$': ('location', coerce_text),
        r'^job description$': ('description', coerce_text),
        r'^job link$': ('link', coerce_text),
        r'^pricing plan$': ('pricing_plan', coerce_pricing_plan),
        r'^approved$': ('approved_at', coerce_date),
        r'^sent$': ('newsletter_at', coerce_date),
        r'^expire[ds]$': ('expires_at', coerce_date),
    }, record)


def coerce(mapping, record):
    job = {}

    for key_pattern, (key_name, key_coerce) in mapping.items():
        key_re = re.compile(key_pattern, re.I)

        for record_key, record_value in record.items():
            if key_re.search(record_key):
                job[key_name] = key_coerce(record_value)

    if job['approved_at'] and not job['expires_at']:
        job['expires_at'] = infer_expires_at(job['approved_at'], job['newsletter_at'])
    job['id'] = create_id(job['posted_at'], job['company_link'])
    job['source'] = 'juniorguru'

    return job


def infer_expires_at(approved_at, newsletter_at=None):
    expires_at = approved_at + timedelta(days=30)
    if newsletter_at:
        return max(expires_at, newsletter_at + timedelta(days=7))
    return expires_at


def coerce_text(value):
    if value:
        return value.strip()


def coerce_boolean_words(value):
    if value is not None:
        return dict(yes=True, no=False).get(value.strip())


def coerce_pricing_plan(value):
    if value and not value.strip().lower().startswith('0 czk'):
        return 'standard'
    return 'community'


def coerce_datetime(value):
    if value:
        value = value.strip()
        try:
            return arrow.get(value, 'M/D/YYYY H:m:s').naive
        except ValueError:
            return arrow.get(datetime.fromisoformat(value)).naive


def coerce_date(value):
    if value:
        value = value.strip()
        try:
            return arrow.get(value, 'M/D/YYYY H:m:s').date()
        except ValueError:
            try:
                return arrow.get(value, 'M/D/YYYY').date()
            except ValueError:
                return datetime.fromisoformat(value).date()


def coerce_boolean(value):
    return bool(value.strip()) if value else False


def coerce_set(value):
    if value:
        items = (item.strip() for item in value.split(','))
        return frozenset(filter(None, items))
    return frozenset()


def create_id(posted_at, company_link):
    url_parts = urlparse(company_link)
    seed = f'{posted_at:%Y-%m-%dT%H:%M:%S} {url_parts.netloc}'
    return hashlib.sha224(seed.encode()).hexdigest()
