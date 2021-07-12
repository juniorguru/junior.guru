import hashlib

from juniorguru.lib.timer import measure
from juniorguru.lib import google_sheets
from juniorguru.lib.coerce import coerce, parse_text, parse_int, parse_date, parse_boolean
from juniorguru.models import Logo, db


@measure('logos')
def main():
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = google_sheets.download(google_sheets.get(doc_key, 'logos'))

    with db:
        Logo.drop_table()
        Logo.create_table()

        for record in records:
            Logo.create(**coerce_record(record))


def coerce_record(record):
    logo = coerce({
        r'^name$': ('name', parse_text),
        r'^filename$': ('filename', parse_text),
        r'^email$': ('email', parse_text),
        r'^link$': ('link', parse_text),
        r'^link regexp$': ('link_re', parse_text),
        r'^months$': ('months', parse_int),
        r'^job slots$': ('job_slots', parse_int),
        r'^starts$': ('starts_at', parse_date),
        r'^expires$': ('expires_at', parse_date),
        r'^email reports$': ('email_reports', parse_boolean),
    }, record)

    logo['id'] = hashlib.sha224(logo['name'].encode()).hexdigest()

    return logo


if __name__ == '__main__':
    main()
