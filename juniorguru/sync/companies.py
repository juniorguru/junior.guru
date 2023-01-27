from pathlib import Path

import click
from strictyaml import Datetime, Map, Optional, Seq, Str, load, Bool, Url

from juniorguru.cli.sync import main as cli
from juniorguru.lib import google_sheets, loggers
from juniorguru.lib.club import parse_coupon
from juniorguru.lib.coerce import (coerce, parse_boolean_words, parse_date, parse_int,
                                   parse_text)
from juniorguru.lib.images import render_image_file
from juniorguru.models.base import db
from juniorguru.models.company import Company


logger = loggers.from_path(__file__)


YAML_PATH = Path(__file__).parent.parent / 'data' / 'companies.yml'

YAML_SCHEMA = Seq(
    Map({
        'name': Str(),
        'slug': Str(),
        'url': Url(),
        Optional('students'): Bool(),
        'collab': Seq(
            Map({
                'plan': Str(),
                'starts_on': Datetime(),
                Optional('expires_on'): Datetime(),
            }),
        ),
    })
)

IMAGES_DIR = Path(__file__).parent.parent / 'images'

POSTERS_DIR = IMAGES_DIR / 'posters-companies'

POSTER_WIDTH = 700

POSTER_HEIGHT = 700


@cli.sync_command()
@click.option('--flush-posters/--no-flush-posters', default=False)
@db.connection_context()
def main(flush_posters):
    if flush_posters:
        logger.warning("Removing all existing posters for companies")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    doc_key = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'
    records = google_sheets.download(google_sheets.get(doc_key, 'companies'))

    logger.info('Setting up companies db table')
    Company.drop_table()
    Company.create_table()

    for record in records:
        logger.info('Saving a record')
        company = Company.create(**coerce_record(record))

    for company in Company.listing():
        logger.info(f"Rendering poster for {company.name}")
        tpl_context = dict(company=company)
        image_path = render_image_file(POSTER_WIDTH, POSTER_HEIGHT,
                                       'company.html', tpl_context, POSTERS_DIR,
                                       prefix=company.slug)
        company.poster_path = image_path.relative_to(IMAGES_DIR)
        company.save()

    # TODO
    logger.info('Reading YAML with companies')
    yaml_records = (record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA))
    list(yaml_records)


def coerce_record(record):
    data = coerce({
        r'^name$': ('name', parse_text),
        r'^filename$': ('logo_filename', parse_text),
        r'^handbook$': ('is_sponsoring_handbook', parse_boolean_words),
        r'^student coupon$': ('student_coupon', parse_text),
        r'^link$': ('url', parse_text),
        r'^coupon$': ('coupon', parse_text),
        r'^starts$': ('starts_on', parse_date),
        r'^expires$': ('expires_on', parse_date),
        r'^job slots$': ('job_slots_count', parse_int),
    }, record)
    if data.get('coupon'):
        data['slug'] = parse_slug(data['coupon'])
    return data


def parse_slug(coupon):
    if coupon:
        return parse_coupon(coupon)['name'].lower()
    return None
