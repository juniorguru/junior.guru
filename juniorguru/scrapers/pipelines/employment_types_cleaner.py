import re


class Pipeline():
    clean_re = re.compile(r'[\-\s]+')
    types_mapping = {
        'fulltime': 'full-time',
        'full time': 'full-time',
        'parttime': 'part-time',
        'part time': 'part-time',
        'contract': 'contract',
        'external collaboration': 'contract',
        'internship': 'internship',
    }

    def process_item(self, item, spider):
        types = (t.lower() for t in item['employment_types'])
        types = (self.types_mapping.get(self.clean_re.sub(' ', t), t)
                 for t in types)
        item['employment_types'] = list(frozenset(types))
        return item
