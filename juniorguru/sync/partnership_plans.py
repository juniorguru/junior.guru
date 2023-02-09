from pathlib import Path

from strictyaml import Int, Map, Optional, Seq, Str, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.partner import PartnershipBenefit, PartnershipPlan


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
    yaml_records = [record.data for record in load(YAML_PATH.read_text(), YAML_SCHEMA)]

    logger.info('Setting up events db tables')
    db.drop_tables([PartnershipPlan, PartnershipBenefit])
    db.create_tables([PartnershipPlan, PartnershipBenefit])

    logger.info('Processing YAML records')
    includes = {}
    for yaml_record in yaml_records:
        benefits = yaml_record.pop('benefits')
        if 'includes' in yaml_record:
            includes[yaml_record['slug']] = yaml_record.pop('includes')

        plan = PartnershipPlan.create(**yaml_record)
        for position, benefit in enumerate(benefits):
            PartnershipBenefit.create(plan=plan, position=position, **benefit)

    logger.info('Recording hierarchy')
    for slug, includes_slug in includes.items():
        plan = PartnershipPlan.get_by_slug(slug)
        plan.includes = PartnershipPlan.get_by_slug(includes_slug)
        plan.save()

    logger.info('Determining and recording hierarchy ranks')
    for yaml_record in yaml_records:
        plan = PartnershipPlan.get_by_slug(yaml_record['slug'])
        plan.hierarchy_rank = list(plan.hierarchy).index(plan)
        plan.save()
