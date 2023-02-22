import re

from juniorguru.sync.jobs_scraped.processing import DropItem


BLOCKLIST = [
    ('title', re.compile(r'plc programátor', re.I)),
    ('title', re.compile(r'elektro', re.I)),
    ('title', re.compile(r'konstruktér', re.I)),
    ('title', re.compile(r'cae inženýr', re.I)),
]


def process(item):
    for field, value_re in BLOCKLIST:
        value = item.get(field) or ''
        if value_re.search(value):
            raise DropItem(f"Blocklist rule applied: {field} value {value!r} matches {value_re.pattern!r}")
    return item
