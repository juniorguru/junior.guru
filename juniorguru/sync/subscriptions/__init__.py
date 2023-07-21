from datetime import date
import itertools
from operator import itemgetter
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import arrow
import click

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.memberful import MemberfulAPI, MemberfulCSV
from juniorguru.models.base import db
from juniorguru.models.feminine_name import FeminineName
from juniorguru.models.partner import Partner
from juniorguru.models.subscription import (SubscriptionActivity,
                                            SubscriptionCancellation,
                                            SubscriptionOrigin, SubscriptionReferrer,
                                            SubscriptionType)


ACTIVITIES_GQL_PATH = Path(__file__).parent / 'activities.gql'

ACTIVITY_TYPES_MAPPING = {
    'new_order': 'order',
    'renewal': 'order',
    'gift_activated': 'order',
    'subscription_deactivated': 'deactivation',
}

SUBSCRIPTIONS_GQL_PATH = Path(__file__).parent / 'subscriptions.gql'

SUBSCRIPTION_TYPES_MAPPING = {
    'THANKYOU': SubscriptionType.FREE,
    'THANKYOUFOREVER': SubscriptionType.FREE,
    'THANKYOUTEAM': SubscriptionType.FREE,
    'PATREON': SubscriptionType.FREE,
    'GITHUB': SubscriptionType.FREE,
    'FOUNDERS': SubscriptionType.FREE,
    'CORESKILL': SubscriptionType.FREE,
    'STUDENTCORESKILL': SubscriptionType.FREE,
    'FINAID': SubscriptionType.FINAID,
}


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['partners', 'feminine-names'])
@click.option('--clear-cache/--keep-cache', default=False)
@click.pass_context
@db.connection_context()
def main(context, clear_cache):
    memberful = MemberfulAPI(cache_dir=context.obj['cache_dir'],
                             clear_cache=clear_cache)

    logger.info('Preparing')
    tables = [SubscriptionActivity, SubscriptionReferrer, SubscriptionOrigin, SubscriptionCancellation]
    db.drop_tables(tables)
    db.create_tables(tables)

    subscripton_types_mapping = {
        **{parse_coupon(coupon)['name']: SubscriptionType.PARTNER
        for coupon in Partner.coupons()},
        **{parse_coupon(coupon)['name']: SubscriptionType.STUDENT
        for coupon in Partner.student_coupons()},
        **SUBSCRIPTION_TYPES_MAPPING
    }

    def has_feminine_name(name) -> bool:
        return FeminineName.is_feminine(name.strip())

    logger.info('Fetching activities from Memberful API')
    query = ACTIVITIES_GQL_PATH.read_text()
    activities = itertools.chain.from_iterable(memberful.get_nodes(query, dict(type=type), delay=0.2)
                                               for type in ACTIVITY_TYPES_MAPPING)
    for activity in logger.progress(activities):
        try:
            account_id = activity['member']['id']
        except (KeyError, TypeError):
            logger.debug('Activity with no account ID, skipping')
        else:
            SubscriptionActivity.add(account_id=account_id,
                                     account_has_feminine_name=has_feminine_name(activity['member']['fullName']),
                                     happened_at=arrow.get(activity['createdAt']).naive,
                                     type=ACTIVITY_TYPES_MAPPING[activity['type']])

    logger.info('Fetching subscriptions from Memberful API')
    subscriptions = memberful.get_nodes(SUBSCRIPTIONS_GQL_PATH.read_text(), delay=0.2)
    for subscription in logger.progress(subscriptions):
        for activity in activities_from_subscription(subscription):
            activity['account_has_feminine_name'] = has_feminine_name(subscription['member']['fullName'])
            try:
                coupon_name = parse_coupon(activity['order_coupon'])['name']
            except TypeError:
                activity['subscription_type'] = None
            else:
                activity['subscription_type'] = subscripton_types_mapping.get(coupon_name)
            SubscriptionActivity.add(**activity)

    SubscriptionActivity.cleanup()
    logger.info(f'Finished with {SubscriptionActivity.count()} activities')

    logger.info("Fetching members data from Memberful CSV")
    memberful = MemberfulCSV(cache_dir=context.obj['cache_dir'], clear_cache=clear_cache)
    for csv_row in memberful.download_csv(dict(type='MembersCsvExport', filter='all')):
        referrer = csv_row['Referrer'] or None
        if referrer:
            referrer_type = get_referrer_type(referrer)
            SubscriptionReferrer.create(account_id=csv_row['Memberful ID'],
                                        name=csv_row['Full Name'],
                                        email=csv_row['Email'],
                                        created_on=date.fromisoformat(csv_row['Created at']),
                                        value=referrer,
                                        type=referrer_type,
                                        is_internal=referrer_type.startswith('/'))
        origin = csv_row['Jak ses dozvěděl(a) o junior.guru?'] or None
        if origin:
            SubscriptionOrigin.create(account_id=csv_row['Memberful ID'],
                                      name=csv_row['Full Name'],
                                      email=csv_row['Email'],
                                      created_on=date.fromisoformat(csv_row['Created at']),
                                      origin=origin)

    logger.info("Fetching cancellations data from Memberful CSV")
    csv_rows = itertools.chain(memberful.download_csv(dict(type='CancellationsCsvExport', filter='all')),
                               memberful.download_csv(dict(type='CancellationsCsvExport', scope='completed', filter='all')))
    for csv_row in csv_rows:
        reason = csv_row['Reason'] or None
        feedback = csv_row['Feedback'] or None
        if reason:
            try:
                date_field_value = csv_row.get('Date') or csv_row.get('Expiration Date')
                expires_on = date.fromisoformat(date_field_value)
            except ValueError:
                logger.warning(f"Invalid date format: {date_field_value!r}")
                expires_on = None
            SubscriptionCancellation.create(name=csv_row['Name'],
                                            email=csv_row['Email'],
                                            expires_on=expires_on,
                                            reason=reason,
                                            feedback=feedback)


def activities_from_subscription(subscription: dict) -> Generator[dict, None, None]:
    account_id = subscription['member']['id']
    subscription_interval = subscription['plan']['intervalUnit']
    subscription_coupon = (subscription['coupon'] or {}).get('code')

    yield dict(account_id=account_id,
               type='order',
               happened_at=arrow.get(subscription['createdAt']).naive,
               subscription_interval=subscription_interval,
               order_coupon=subscription_coupon)
    if subscription['trialStartAt']:
        yield dict(account_id=account_id,
                   type='trial_start',
                   happened_at=arrow.get(subscription['trialStartAt']).naive,
                   subscription_interval=subscription_interval,
                   order_coupon=subscription_coupon)
    if subscription['trialEndAt']:
        yield dict(account_id=account_id,
                   type='trial_end',
                   happened_at=arrow.get(subscription['trialEndAt']).naive,
                   subscription_interval=subscription_interval,
                   order_coupon=subscription_coupon)

    orders = sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True)
    for i, order in enumerate(orders):
        if subscription_coupon and i == 0:
            order_coupon = subscription_coupon
        else:
            order_coupon = (order['coupon'] or {}).get('code')

        yield dict(account_id=account_id,
                   type='order',
                   happened_at=arrow.get(order['createdAt']).naive,
                   subscription_interval=subscription['plan']['intervalUnit'],
                   order_coupon=order_coupon)


def get_referrer_type(url: str) -> str:
    parts = urlparse(url)
    if parts.netloc == 'junior.guru':
        return parts.path.rstrip('/') or '/'
    if parts.netloc == 't.co':
        return 'twitter'
    if parts.netloc == 'honzajavorek.cz':
        if '/blog/' in url and 'poznamky' in url:
            return 'weeknotes'
        return 'honzajavorek'
    domain = parts.netloc.split('.')[-2]
    if domain in ('google', 'facebook', 'linkedin', 'youtube'):
        return domain
    return 'other'
