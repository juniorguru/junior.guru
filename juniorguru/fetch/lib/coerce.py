import re
from datetime import datetime

import arrow


def coerce(mapping, record):
    data = {}
    for key_pattern, (key_name, key_coerce) in mapping.items():
        key_re = re.compile(key_pattern, re.I)
        for record_key, record_value in record.items():
            if key_re.search(record_key):
                data[key_name] = key_coerce(record_value)
    return data


def parse_text(value):
    if value:
        return value.strip()


def parse_int(value):
    if value:
        try:
            value = value.strip()
        except AttributeError:
            pass
        return int(value)


def parse_boolean_words(value):
    if value is not None:
        return dict(yes=True, no=False).get(value.strip())


def parse_datetime(value):
    if value:
        value = value.strip()
        try:
            return arrow.get(value, 'M/D/YYYY H:m:s').naive
        except ValueError:
            return arrow.get(datetime.fromisoformat(value)).naive


def parse_date(value):
    if value:
        value = value.strip()
        try:
            return arrow.get(value, 'M/D/YYYY H:m:s').date()
        except ValueError:
            try:
                return arrow.get(value, 'M/D/YYYY').date()
            except ValueError:
                return datetime.fromisoformat(value).date()


def parse_boolean(value):
    return bool(value.strip()) if value else False


def parse_set(value):
    if value:
        items = (item.strip() for item in value.split(','))
        return frozenset(filter(None, items))
    return frozenset()
