import re

from juniorguru.models.job import EMPLOYMENT_TYPES


STOP_WORDS = [
    re.compile(r'\bwork\b'),
    re.compile(r'\bpráce\s+na\b'),
    re.compile(r'\bpráce\b'),
]

SEPARATORS_RE = re.compile(r'[\-\s]+')

EMPLOYMENT_TYPES_MAPPING = {
    'fulltime': 'FULL_TIME',
    'parttime': 'PART_TIME',
    'external_collaboration': 'CONTRACT',
    'plný_úvazek': 'FULL_TIME',
    'částečný_úvazek': 'PART_TIME',
    'zkrácený_úvazek': 'PART_TIME',
    'placená_stáž': 'PAID_INTERNSHIP',
    'neplacená_stáž': 'UNPAID_INTERNSHIP',
    'stáž': 'INTERNSHIP',
    'dobrovolnictví': 'VOLUNTEERING',
}


def process(item):
    if item.get('employment_types'):
        item['employment_types'] = clean_employment_types(item['employment_types'])
    return item


def clean_employment_types(employment_types):
    employment_types = map(clean_employment_type, employment_types)
    return sorted(set(filter(None, employment_types)))


def clean_employment_type(employment_type):
    value = employment_type.lower()
    for stop_word_re in STOP_WORDS:
        value = stop_word_re.sub('', value)
    mapping_key = SEPARATORS_RE.sub('_', value.strip())
    value = EMPLOYMENT_TYPES_MAPPING.get(mapping_key, mapping_key.upper())
    return value if value in EMPLOYMENT_TYPES else None
