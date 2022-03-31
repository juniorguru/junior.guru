import os
from pathlib import Path

from juniorguru.lib.tasks import sync_task
from juniorguru.lib import google_sheets
from juniorguru.lib.coerce import coerce, parse_boolean_words, parse_text, parse_date
from juniorguru.models import Company, db
from juniorguru.lib import loggers
from juniorguru.lib.images import render_image_file


logger = loggers.get(__name__)


FLUSH_POSTERS_COMPANIES = bool(int(os.getenv('FLUSH_POSTERS_COMPANIES', 0)))
IMAGES_DIR = Path(__file__).parent.parent / 'images'
POSTERS_DIR = IMAGES_DIR / 'posters-companies'

POSTER_WIDTH = 700
POSTER_HEIGHT = 700


@sync_task()
@db.connection_context()
def main():
    if FLUSH_POSTERS_COMPANIES:
        logger.warning("Removing all existing posters for companies, FLUSH_POSTERS_COMPANIES is set")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = google_sheets.download(google_sheets.get(doc_key, 'companies'))

    Company.drop_table()
    Company.create_table()

    for record in records:
        logger.info('Saving a record')
        company = Company.create(**coerce_record(record))

        logger.info(f"Rendering images for '{company.name}'")
        tpl_context = dict(company=company)
        render_image_file(POSTER_WIDTH, POSTER_HEIGHT,
                          'company.html', tpl_context, POSTERS_DIR)


def coerce_record(record):
    return coerce({
        r'^name$': ('name', parse_text),
        r'^email$': ('email', parse_text),
        r'^filename$': ('logo_filename', parse_text),
        r'^handbook$': ('is_sponsoring_handbook', parse_boolean_words),
        r'^student coupon base$': ('student_coupon_base', parse_text),
        r'^link$': ('link', parse_text),
        r'^coupon base$': ('coupon_base', parse_text),
        r'^starts$': ('starts_on', parse_date),
        r'^expires$': ('expires_on', parse_date),
    }, record)
