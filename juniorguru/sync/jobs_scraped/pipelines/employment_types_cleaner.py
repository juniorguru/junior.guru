import re

from juniorguru.models.job import EMPLOYMENT_TYPES


CLEAN_RE = re.compile(r'[\-\s]+')

EMPLOYMENT_TYPES_MAPPING = {
    'FULLTIME': 'FULL_TIME',
    'PARTTIME': 'PART_TIME',
    'EXTERNAL_COLLABORATION': 'CONTRACT',
    'PLNÝ_ÚVAZEK': 'FULL_TIME',
    'ČÁSTEČNÝ_ÚVAZEK': 'PART_TIME',
    'PLACENÁ_STÁŽ': 'PAID_INTERNSHIP',
    'NEPLACENÁ_STÁŽ': 'UNPAID_INTERNSHIP',
    'STÁŽ': 'INTERNSHIP',
    'DOBROVOLNICTVÍ': 'VOLUNTEERING',
}


def process(item):
    if item.get('employment_types'):
        item['employment_types'] = clean(item['employment_types'])
    return item


def clean(employment_types):
    employment_types = (CLEAN_RE.sub('_', t.upper())
                        for t in employment_types)
    employment_types = (EMPLOYMENT_TYPES_MAPPING.get(t, t)
                        for t in employment_types)
    employment_types = (t for t in employment_types
                        if t in EMPLOYMENT_TYPES)
    return list(set(employment_types))
