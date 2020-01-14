import re
import hashlib
from urllib.parse import urlparse

import arrow


def coerce_record(record):
    return coerce({
        r'^timestamp$': ('timestamp', coerce_timestamp),
        r'^company name$': ('company_name', coerce_text),
        r'^job type$': ('job_type', coerce_text),
        r'^job title$': ('title', coerce_text),
        r'^company website link$': ('company_link', coerce_text),
        r'^email address$': ('email', coerce_text),
        r'^job location$': ('location', coerce_text),
        r'^job description$': ('description', coerce_text),
        r'^job link$': ('job_link', coerce_text),
        r'^approved$': ('is_approved', coerce_boolean),
        r'^sent$': ('is_sent', coerce_boolean),
    }, record)


def coerce(mapping, record):
    job = {}

    for key_pattern, (key_name, key_coerce) in mapping.items():
        key_re = re.compile(key_pattern, re.I)

        for record_key, record_value in record.items():
            if key_re.search(record_key):
                job[key_name] = key_coerce(record_value)

    job['id'] = create_id(job['timestamp'], job['company_link'])
    return job


def coerce_text(value):
    if value:
        return value.strip()


def coerce_boolean_words(value):
    if value is not None:
        return dict(yes=True, no=False).get(value.strip())


def coerce_timestamp(value):
    if value:
        return arrow.get(value.strip(), 'M/D/YYYY H:m:s').naive


def coerce_boolean(value):
    return bool(value.strip()) if value else False


def create_id(timestamp, company_link):
    parse_result = urlparse(company_link)
    seed = f'{timestamp:%Y-%m-%dT%H:%M:%S} {parse_result.netloc}'
    return hashlib.sha224(seed.encode()).hexdigest()
