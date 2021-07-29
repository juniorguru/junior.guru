from juniorguru.lib.timer import measure
from juniorguru.lib import google_sheets
from juniorguru.lib.coerce import coerce, parse_text, parse_date, parse_boolean
from juniorguru.models import Company, db


@measure('companies')
def main():
    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = google_sheets.download(google_sheets.get(doc_key, 'companies'))

    with db:
        Company.drop_table()
        Company.create_table()

        for record in records:
            Company.create(**coerce_record(record))


def coerce_record(record):
    return coerce({
        r'^name$': ('name', parse_text),
        r'^email$': ('email', parse_text),
        r'^filename$': ('filename', parse_text),
        r'^handbook$': ('is_sponsoring_handbook', parse_boolean),
        r'^sponsored coupon$': ('has_students', parse_boolean),
        r'^link$': ('link', parse_text),
        r'^coupon$': ('coupon', parse_text),
        r'^starts$': ('starts_at', parse_date),
        r'^expires$': ('expires_at', parse_date),
    }, record)


if __name__ == '__main__':
    main()
