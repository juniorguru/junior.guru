from datetime import timedelta
from operator import itemgetter
from pathlib import Path
from typing import Any, Generator

import arrow

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.memberful import Memberful
from juniorguru.models.base import db
from juniorguru.models.feminine_name import FeminineName
from juniorguru.models.partner import Partner
from juniorguru.models.subscription import SubscribedPeriodType, SubscribedPeriod


MEMBERS_GQL_PATH = Path(__file__).parent / 'members.gql'

SUBSCRIBED_PERIOD_TYPES_MAPPING = {
    'THANKYOU': SubscribedPeriodType.FREE,
    'THANKYOUFOREVER': SubscribedPeriodType.FREE,
    'THANKYOUTEAM': SubscribedPeriodType.FREE,
    'PATREON': SubscribedPeriodType.FREE,
    'GITHUB': SubscribedPeriodType.FREE,
    'FOUNDERS': SubscribedPeriodType.FREE,
    'CORESKILL': SubscribedPeriodType.FREE,
    'STUDENTCORESKILL': SubscribedPeriodType.FREE,
    'FINAID': SubscribedPeriodType.FINAID,
}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['partners', 'feminine-names'])
@db.connection_context()
def main():
    memberful = Memberful()

    logger.info('Preparing subscribed periods table')
    SubscribedPeriod.drop_table()
    SubscribedPeriod.create_table()

    logger.info('Mapping coupons to subscribed period types')
    subscribed_period_types_mapping = {
        **{parse_coupon(coupon)['name']: SubscribedPeriodType.PARTNER
        for coupon in Partner.coupons()},
        **{parse_coupon(coupon)['name']: SubscribedPeriodType.STUDENT
        for coupon in Partner.student_coupons()},
        **SUBSCRIBED_PERIOD_TYPES_MAPPING
    }

    logger.info('Fetching all subscriptions from Memberful')
    members = memberful.get_nodes(MEMBERS_GQL_PATH.read_text())
    for member in members:
        logger.info(f'Processing member #{member["id"]} (subscriptions: {len(member["subscriptions"])})')
        name = member['fullName'].strip()
        has_feminine_name = FeminineName.is_feminine(name)

        for subscription in member['subscriptions']:
            logger.debug(f'Processing subscription #{subscription["id"]}')
            for n, subscribed_period in enumerate(get_subscribed_periods(subscription), start=1):
                logger.debug(f'Processing subscribed period #{n}: {subscribed_period!r}')
                if subscribed_period['coupon']:
                    coupon_name = parse_coupon(subscribed_period['coupon'])['name']
                    type = subscribed_period_types_mapping.get(coupon_name, SubscribedPeriodType.INDIVIDUALS)
                elif subscribed_period['is_trial']:
                    type = SubscribedPeriodType.TRIAL
                else:
                    type = SubscribedPeriodType.INDIVIDUALS
                SubscribedPeriod.create(account_id=member['id'],
                                        start_on=subscribed_period['start_on'],
                                        end_on=subscribed_period['end_on'],
                                        interval_unit=subscription['plan']['intervalUnit'],
                                        has_feminine_name=has_feminine_name,
                                        type=type)


def get_subscribed_periods(subscription: dict) -> Generator[dict[str, Any], None, None]:
    orders = list(sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True))
    renewal_on = arrow.get(subscription['expiresAt']).date()

    if subscription.get('trialStartAt') and subscription.get('trialEndAt'):
        trial = (arrow.get(subscription['trialStartAt']).date(),
                 arrow.get(subscription['trialEndAt']).date() - timedelta(days=1))
    else:
        trial = None

    for i, order in enumerate(orders):
        start_on = arrow.get(order['createdAt']).date()
        end_on = renewal_on - timedelta(days=1)
        is_trial = ((start_on, end_on) == trial) if trial else False

        if subscription['coupon'] and i == 0:
            coupon = subscription['coupon']
        else:
            coupon = order['coupon']
        coupon = (coupon or {}).get('code')

        yield dict(start_on=start_on, end_on=end_on, is_trial=is_trial, coupon=coupon)
        renewal_on = start_on
