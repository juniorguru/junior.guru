import re

from juniorguru.models import EMPLOYMENT_TYPES


class Pipeline():
    clean_re = re.compile(r'[\-\s]+')
    types_mapping = {
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

    def process_item(self, item, spider):
        if item.get('employment_types'):
            types = (self.clean_re.sub('_', t.upper())
                    for t in item['employment_types'])
            types = (self.types_mapping.get(t, t) for t in types)
            types = (t for t in types if t in EMPLOYMENT_TYPES)
            item['employment_types'] = list(set(types))
        return item
