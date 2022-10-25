import re
from datetime import datetime

import arrow

from juniorguru.lib import loggers
from juniorguru.lib.memberful import MEMBERFUL_MUTATIONS_ENABLED, Memberful
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.company import Company


logger = loggers.get(__name__)


@cli.sync_command(requires=['subscriptions',
                        'companies'])
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

    paying_companies = (company for company in Company.listing()
                        if company.expires_on)
    for company in paying_companies:
        logger_c = logger[re.sub('\W', '', company.name).lower()]
        logger_c.info(f'Company subscription expires on {company.expires_on}')
        for employee in company.list_members:
            logger_c.debug(f'Processing {employee.display_name}')
            if employee.expires_at.date() < company.expires_on:
                logger_c.warning(f'{employee!r} {employee.expires_at.date()} < {company.expires_on}')
                if MEMBERFUL_MUTATIONS_ENABLED:
                    params = dict(id=employee.memberful_subscription_id,
                                  expiresAt=int(arrow.get(company.expires_on).timestamp()))
                    memberful.mutate(mutation, params)
                    employee.expires_at = datetime.combine(company.expires_on, datetime.min.time())
                    employee.save()
                    logger_c.info(f'{employee!r} subscription updated to expire on {employee.expires_at.date()}')
                else:
                    logger_c.warning('Memberful mutations not enabled')
            else:
                logger_c.debug(f'{employee!r} {employee.expires_at.date()} ≥ {company.expires_on}')
