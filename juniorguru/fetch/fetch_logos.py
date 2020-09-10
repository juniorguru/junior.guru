import re
import hashlib
from urllib.parse import urlparse

from juniorguru.fetch.lib.google import download_sheet
from juniorguru.fetch.lib.coerce import coerce, parse_text, parse_int, parse_date
from juniorguru.models import Logo, db


def main():
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = download_sheet(doc_key, 'logos')

    with db:
        Logo.drop_table()
        Logo.create_table()

        for record in records:
            Logo.create(**coerce_record(record))


def coerce_record(record):
    logo = coerce({
        r'^name$': ('name', parse_text),
        r'^email$': ('email', parse_text),
        r'^link$': ('link', parse_text),
        r'^link regexp$': ('link_re', parse_text),
        r'^months$': ('months', parse_int),
        r'^starts$': ('starts_at', parse_date),
        r'^expires$': ('expires_at', parse_date),
    }, record)

    logo['id'] = hashlib.sha224(logo['name'].encode()).hexdigest()
    if logo['link_re'] is None:
        logo['link_re'] = re.escape(urlparse(logo['link']).netloc)

    return logo


if __name__ == '__main__':
    main()
