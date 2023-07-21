from datetime import datetime

import arrow

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers, mutations
from juniorguru.lib.memberful import MemberfulAPI
from juniorguru.models.base import db
from juniorguru.models.partner import Partnership


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['subscriptions', 'partners'])
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

    for partnership in Partnership.active_listing(include_barters=False):
        partner = partnership.partner
        logger_c = logger[partner.slug]
        logger_c.info(f'Partnership expires on {partnership.expires_on}')
        for employee in partner.list_members:
            logger_c.debug(f'Processing {employee.display_name}')
            if employee.expires_at.date() < partnership.expires_on:
                logger_c.warning(f'{employee!r} {employee.expires_at.date()} < {partnership.expires_on}')
                params = dict(id=employee.subscription_id,
                              expiresAt=int(arrow.get(partnership.expires_on).timestamp()))
                if align_subscription(memberful, mutation, params):
                    employee.expires_at = datetime.combine(partnership.expires_on, datetime.min.time())
                    employee.save()
                    logger_c.info(f'{employee!r} subscription updated to expire on {employee.expires_at.date()}')
            else:
                logger_c.debug(f'{employee!r} {employee.expires_at.date()} ≥ {partnership.expires_on}')


@mutations.mutates_memberful()
def align_subscription(memberful, mutation, params):
    return memberful.mutate(mutation, params)
