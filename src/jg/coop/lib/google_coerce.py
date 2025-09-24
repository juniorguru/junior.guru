import re
from datetime import datetime
from urllib.parse import urlparse


def coerce(mapping, record):
    data = {}
    for key_pattern, (key_name, key_coerce) in mapping.items():
        key_re = re.compile(key_pattern, re.I)
        for record_key, record_value in record.items():
            if key_re.search(record_key):
                value = key_coerce(record_value)
                if value is not None:
                    data[key_name] = value
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
        return dict(yes=True, no=False, ano=True, ne=False, true=True, false=False).get(
            value.strip().lower()
        )


def parse_datetime(value):
    if value:
        value = value.strip()
        try:
            return datetime.strptime(value, "%m/%d/%Y %H:%M:%S")
        except ValueError:
            return datetime.fromisoformat(value).replace(tzinfo=None)


def parse_date(value):
    if value:
        value = value.strip()
        try:
            return datetime.strptime(value, "%m/%d/%Y %H:%M:%S").date()
        except ValueError:
            try:
                return datetime.strptime(value, "%m/%d/%Y").date()
            except ValueError:
                return datetime.fromisoformat(value).date()


def parse_boolean(value):
    return bool(value.strip()) if value else False


def parse_set(value):
    if value:
        items = (item.strip() for item in value.split(","))
        return frozenset(filter(None, items))
    return frozenset()


def parse_url(value):
    if value:
        url = value.strip()
        url_parts = urlparse(url)
        if not url_parts.scheme:
            raise ValueError(f"{url} doesn't look like a valid URL")
        if url_parts.scheme.lower() not in ["http", "https"]:
            raise ValueError(f"{url} doesn't look like a valid URL")
        if not url_parts.netloc:
            raise ValueError(f"{url} doesn't look like a valid URL")
        return url
