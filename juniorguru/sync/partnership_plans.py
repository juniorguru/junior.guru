from pathlib import Path

from strictyaml import Map, Optional, Seq, Str, load, Int

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.company import PartnershipPlan, PartnershipBenefit


logger = loggers.from_path(__file__)


YAML_PATH = Path('juniorguru/data/partnership-plans.yml')

YAML_SCHEMA = Seq(
    Map({
        'slug': Str(),
        'name': Str(),
        Optional('includes'): Str(),
        'benefits': Seq(
            Map({
                'text': Str(),
                'icon': Str(),
                Optional('slug'): Str(),
                Optional('quantity'): Int(),
            }),
        ),
        'price': Int(),
        Optional('limit'): Int(),
    })
)


@cli.sync_command()
@db.connection_context()
def main():
    logger.info('Reading YAML with partners')
    yaml_records = (record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA))

    logger.info('Setting up events db tables')
    db.drop_tables([PartnershipPlan, PartnershipBenefit])
    db.create_tables([PartnershipPlan, PartnershipBenefit])

    logger.info('Processing YAML records')
    hierarchy = {}
    for yaml_record in yaml_records:
        benefits = yaml_record.pop('benefits')
        if 'includes' in yaml_record:
            hierarchy[yaml_record['slug']] = yaml_record.pop('includes')

        plan = PartnershipPlan.create(**yaml_record)
        for benefit in benefits:
            PartnershipBenefit.create(plan=plan, **benefit)

    for slug, includes_slug in hierarchy.items():
        plan = PartnershipPlan.get_by_slug(slug)
        plan.includes = PartnershipPlan.get_by_slug(includes_slug)
        plan.save()
