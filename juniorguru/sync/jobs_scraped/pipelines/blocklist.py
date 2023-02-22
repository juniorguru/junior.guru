import re

from juniorguru.sync.jobs_scraped.processing import DropItem


BLOCKLIST = [
    ('company_name', re.compile(r'BEKO Engineering', re.I)),
]


def process(item):
    for field, value_re in BLOCKLIST:
        value = item.get(field) or ''
        if value_re.search(value):
            raise DropItem(f"Blocklist rule applied: {field} value {value!r} matches {value_re.pattern!r}")
    return item
