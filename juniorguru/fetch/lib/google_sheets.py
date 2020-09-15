import string

import gspread

from juniorguru.fetch.lib.google import get_credentials


def get(doc_key, sheet_name):
    credentials = get_credentials([
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ])
    doc = gspread.authorize(credentials).open_by_key(doc_key)
    return doc.worksheet(sheet_name)


def download(sheet):
    return sheet.get_all_records(default_blank=None)


def upload(sheet, records):
    current_rows = sheet.get_all_values()
    if current_rows:
        range = get_range_notation(current_rows)
        sheet.update(range, [['' for cell in row] for row in current_rows])

    new_rows = records_to_rows(records)
    range = get_range_notation(new_rows)
    sheet.update(range, new_rows)


def get_range_notation(rows):
    rows_count = len(rows)
    if not rows_count:
        raise ValueError('No rows')
    cols_count = len(rows[0])
    if not cols_count:
        raise ValueError('No columns')
    return f'A1:{string.ascii_uppercase[cols_count - 1]}{rows_count}'


def records_to_rows(records):
    # can't use set here as the order is significant
    tmp = {}
    for record in records:
        for key in record:
            tmp[key] = None
    keys = list(tmp.keys())

    rows = [keys]
    for record in records:
        rows.append([record.get(key) for key in keys])
    return rows
