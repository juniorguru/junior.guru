from datetime import timedelta
import itertools
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
from juniorguru.models.subscription import SubscribedPeriodType, SubscriptionActivity, SubscriptionActivityType, SubscribedPeriod


MEMBERS_GQL_PATH = Path(__file__).parent / 'members.gql'

ACTIVITIES_GQL_PATH = Path(__file__).parent / 'activities.gql'

ACTIVITY_TYPES_MAPPING = {
    'new_order': SubscriptionActivityType.BEGIN,
    'new_gift': SubscriptionActivityType.BEGIN,
    'subscription_deleted': SubscriptionActivityType.END,
    'member_deleted': SubscriptionActivityType.END,
    'subscription_deactivated': SubscriptionActivityType.END,
}

SUBSCRIBED_PERIOD_TYPES_MAPPING = {
    'THANKYOU': SubscribedPeriodType.FREE,
    'THANKYOUFOREVER': SubscribedPeriodType.FREE,
    'THANKYOUTEAM': SubscribedPeriodType.TEAM,
    'PATREON': SubscribedPeriodType.FREE,
    'GITHUB': SubscribedPeriodType.FREE,
    'FOUNDERS': SubscribedPeriodType.FREE,
    'FINAID': SubscribedPeriodType.FINAID,
    'CORESKILL': SubscribedPeriodType.CORESKILL,
    'STUDENTCORESKILL': SubscribedPeriodType.CORESKILL,
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

    logger.info('Preparing subscription activity table')
    SubscriptionActivity.drop_table()
    SubscriptionActivity.create_table()

    logger.info('Fetching activity log entries from Memberful')
    query = ACTIVITIES_GQL_PATH.read_text()
    activities = itertools.chain(memberful.get_nodes(query, dict(type='new_order')),
                                 memberful.get_nodes(query, dict(type='new_gift')),
                                 memberful.get_nodes(query, dict(type='subscription_deleted')),
                                 memberful.get_nodes(query, dict(type='member_deleted')),
                                 memberful.get_nodes(query, dict(type='subscription_deactivated')))
    for activity in activities:
        try:
            account_id = activity['member']['id']
        except (KeyError, TypeError):
            account_id = None
        activity_type = ACTIVITY_TYPES_MAPPING[activity['type']]
        happening_on = arrow.get(activity['createdAt']).date()
        logger.info(f"Saving {activity_type.upper()} activity for account {format_account_id(account_id)}, {happening_on}")
        SubscriptionActivity.create(account_id=account_id,
                                    happening_on=happening_on,
                                    type=activity_type)
    count = SubscriptionActivity.delete_duplicates()
    logger.info(f"Deleted {count} duplicates")


def format_account_id(account_id: str) -> str:
    return f"#{account_id}" if account_id else '(deleted)'


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
