from datetime import datetime

import arrow

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.memberful import MEMBERFUL_MUTATIONS_ENABLED, Memberful
from juniorguru.models.base import db
from juniorguru.models.partner import Company


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['subscriptions', 'companies'])
@db.connection_context()
def main():
    memberful = Memberful()
    mutation = '''
        mutation ($id: ID!, $expiresAt: Int!) {
            subscriptionChangeExpirationTime(id: $id, expiresAt: $expiresAt) {
                subscription {
                    id
                    expiresAt
                }
            }
        }
    '''

    for company in Company.active_listing(include_barters=False):
        logger_c = logger[company.slug]
        partnership = company.active_partnership()
        logger_c.info(f'Company partnership expires on {partnership.expires_on}')
        for employee in company.list_members:
            logger_c.debug(f'Processing {employee.display_name}')
            if employee.expires_at.date() < partnership.expires_on:
                logger_c.warning(f'{employee!r} {employee.expires_at.date()} < {partnership.expires_on}')
                if MEMBERFUL_MUTATIONS_ENABLED:
                    params = dict(id=employee.subscription_id,
                                  expiresAt=int(arrow.get(company.expires_on).timestamp()))
                    memberful.mutate(mutation, params)
                    employee.expires_at = datetime.combine(partnership.expires_on, datetime.min.time())
                    employee.save()
                    logger_c.info(f'{employee!r} subscription updated to expire on {employee.expires_at.date()}')
                else:
                    logger_c.warning('Memberful mutations not enabled')
            else:
                logger_c.debug(f'{employee!r} {employee.expires_at.date()} ≥ {partnership.expires_on}')
