import re

from juniorguru.models import EMPLOYMENT_TYPES


CLEAN_RE = re.compile(r'[\-\s]+')

TYPES_MAPPING = {
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
        types = (CLEAN_RE.sub('_', t.upper())
                for t in item['employment_types'])
        types = (TYPES_MAPPING.get(t, t) for t in types)
        types = (t for t in types if t in EMPLOYMENT_TYPES)
        item['employment_types'] = list(set(types))
    return item
