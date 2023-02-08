from collections import defaultdict
from datetime import date
from pathlib import Path

import click
from strictyaml import Bool, Map, Optional, Seq, Str, Url, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.club import parse_coupon
from juniorguru.lib.images import render_image_file
from juniorguru.lib.memberful import Memberful
from juniorguru.lib.yaml import Date
from juniorguru.models.base import db
from juniorguru.models.partner import Partner, Partnership, PartnershipPlan


logger = loggers.from_path(__file__)


YAML_PATH = Path('juniorguru/data/partners.yml')

YAML_SCHEMA = Seq(
    Map({
        'name': Str(),
        'slug': Str(),
        'url': Url(),
        Optional('students'): Bool(),
        'partnerships': Seq(
            Map({
                'plan': Str(),
                'starts_on': Date(),
                Optional('expires_on'): Date(),
                Optional('benefits'): Seq(
                    Map({
                        'slug': Str(),
                        Optional('done'): Url() | Bool(),
                    })
                ),
                Optional('agreements'): Seq(
                    Map({
                        'text': Str(),
                        Optional('done'): Url() | Bool(),
                    })
                ),
            }),
        ),
    })
)

IMAGES_DIR = Path('juniorguru/images')

LOGOS_DIR = IMAGES_DIR / 'logos'

POSTERS_DIR = IMAGES_DIR / 'posters-partners'

POSTER_WIDTH = 700

POSTER_HEIGHT = 700


@cli.sync_command(dependencies=['partnership-plans'])
@click.option('--flush-posters/--no-flush-posters', default=False)
@db.connection_context()
def main(flush_posters):
    if flush_posters:
        logger.warning("Removing all existing posters for partners")
        for poster_path in POSTERS_DIR.glob('*.png'):
            poster_path.unlink()

    logger.info('Getting coupons data from Memberful')
    memberful = Memberful()
    coupons_mapping = get_coupons_mapping(memberful.get_nodes('coupons', 'code, state'))

    logger.info('Reading YAML with partners')
    yaml_records = (record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA))

    logger.info('Setting up events db tables')
    db.drop_tables([Partner, Partnership])
    db.create_tables([Partner, Partnership])

    logger.info('Processing YAML records')
    for yaml_record in yaml_records:
        partnerships = yaml_record.pop('partnerships')

        logo_path = LOGOS_DIR / f"{yaml_record['slug']}.svg"
        if not logo_path.exists():
            logo_path = logo_path.with_suffix('.png')
        if not logo_path.exists():
            raise FileNotFoundError(f"'There is no {yaml_record['slug']}.svg or .png inside {LOGOS_DIR}")

        partner = Partner.create(logo_path=logo_path.relative_to(IMAGES_DIR),
                                 **yaml_record,
                                 **coupons_mapping.get(yaml_record['slug'], {}))
        for partnership in partnerships:
            try:
                plan_slug = partnership.pop('plan')
                partnership['plan'] = PartnershipPlan.get_by_slug(plan_slug)
            except PartnershipPlan.DoesNotExist:
                if not partnership['expires_on'] or partnership['expires_on'] > date.today():
                    raise
                logger.warning(f"Expired {partner.name} partnership has non-existing plan: {plan_slug}")
            Partnership.create(partner=partner, **partnership)

    for partner in Partner.active_listing():
        logger.info(f"Rendering poster for {partner.name}")
        tpl_context = dict(partner=partner)
        image_path = render_image_file(POSTER_WIDTH, POSTER_HEIGHT,
                                       'partner.html', tpl_context, POSTERS_DIR,
                                       prefix=partner.slug)
        partner.poster_path = image_path.relative_to(IMAGES_DIR)
        partner.save()

    logger.info('Checking expired partnerships for leftovers')
    for partner in Partner.expired_listing():
        logo_path = IMAGES_DIR / partner.logo_path
        if logo_path.exists():
            logger.warning(f"File {logo_path} is probably redundant, partnership with {partner.name} expired")


def get_coupons_mapping(coupons):
    coupons_mapping = defaultdict(dict)
    for coupon in coupons:
        if coupon['state'] == 'enabled':
            parts = parse_coupon(coupon['code'])
            slug = parts['name'].lower().removeprefix('student')
            field = 'student_coupon' if parts['is_student'] else 'coupon'
            coupons_mapping[slug][field] = coupon['code']
    return dict(coupons_mapping)
