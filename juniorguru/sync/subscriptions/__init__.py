import itertools
import re
from datetime import date
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
                                            SubscriptionActivityType,
                                            SubscriptionCancellation,
                                            SubscriptionMarketingSurvey,
                                            SubscriptionReferrer, SubscriptionType)


ACTIVITIES_GQL_PATH = Path(__file__).parent / 'activities.gql'

ACTIVITY_TYPES_MAPPING = {
    'new_order': SubscriptionActivityType.ORDER,
    'renewal': SubscriptionActivityType.ORDER,
    'gift_activated': SubscriptionActivityType.ORDER,
    'subscription_deactivated': SubscriptionActivityType.DEACTIVATION,
    'subscription_deleted': SubscriptionActivityType.DEACTIVATION,
    'order_suspended': SubscriptionActivityType.DEACTIVATION,
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
    tables = [SubscriptionActivity, SubscriptionReferrer, SubscriptionMarketingSurvey, SubscriptionCancellation]
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
            happened_at = arrow.get(activity['createdAt']).naive
            SubscriptionActivity.add(account_id=account_id,
                                     account_has_feminine_name=has_feminine_name(activity['member']['fullName']),
                                     happened_on=happened_at.date(),
                                     happened_at=happened_at,
                                     source=f"activity#{activity['id']}/{activity['type']}",
                                     type=ACTIVITY_TYPES_MAPPING[activity['type']])
    logger.info('Fetching subscriptions from Memberful API')
    subscriptions = memberful.get_nodes(SUBSCRIPTIONS_GQL_PATH.read_text(), delay=0.2)
    for subscription in logger.progress(subscriptions):
        for activity in activities_from_subscription(subscription):
            activity['account_has_feminine_name'] = has_feminine_name(subscription['member']['fullName'])
            try:
                coupon_name = parse_coupon(activity['order_coupon'])['name']
                activity['subscription_type'] = subscripton_types_mapping[coupon_name]
            except (TypeError, KeyError):
                activity['subscription_type'] = SubscriptionType.INDIVIDUAL
            SubscriptionActivity.add(**activity)
    logger.info('Identifying trials and updating their subscription type')
    SubscriptionActivity.mark_trials()
    logger.info(f'Finished with {SubscriptionActivity.total_count()} activities')

    logger.info("Fetching members data from Memberful CSV")
    memberful = MemberfulCSV(cache_dir=context.obj['cache_dir'], clear_cache=clear_cache)
    for csv_row in memberful.download_csv(dict(type='MembersCsvExport', filter='all')):
        referrer = csv_row['Referrer'] or None
        if referrer:
            referrer_type = classify_referrer(referrer)
            SubscriptionReferrer.create(account_id=csv_row['Memberful ID'],
                                        name=csv_row['Full Name'],
                                        email=csv_row['Email'],
                                        created_on=date.fromisoformat(csv_row['Created at']),
                                        value=referrer,
                                        type=referrer_type,
                                        is_internal=referrer_type.startswith('/'))
        marketing_survey_answer = csv_row['Jak ses dozvěděl(a) o junior.guru?'] or None
        if marketing_survey_answer:
            marketing_survey_answer_type = classify_marketing_survey_answer(marketing_survey_answer)
            SubscriptionMarketingSurvey.create(account_id=csv_row['Memberful ID'],
                                               name=csv_row['Full Name'],
                                               email=csv_row['Email'],
                                               created_on=date.fromisoformat(csv_row['Created at']),
                                               value=marketing_survey_answer,
                                               type=marketing_survey_answer_type)

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

    created_at = arrow.get(subscription['createdAt']).naive
    yield dict(account_id=account_id,
               type='order',
               source=f"subscription#{subscription['id']}/created_at",
               happened_on=created_at.date(),
               happened_at=created_at,
               subscription_interval=subscription_interval,
               order_coupon=subscription_coupon)
    if subscription['trialStartAt']:
        trial_start_at = arrow.get(subscription['trialStartAt']).naive
        yield dict(account_id=account_id,
                   type='trial_start',
                   source=f"subscription#{subscription['id']}/trial_start_at",
                   happened_on=trial_start_at.date(),
                   happened_at=trial_start_at,
                   subscription_interval=subscription_interval,
                   order_coupon=subscription_coupon)
    if subscription['trialEndAt']:
        trial_end_at = arrow.get(subscription['trialEndAt']).naive
        yield dict(account_id=account_id,
                   type='trial_end',
                   source=f"subscription#{subscription['id']}/trial_end_at",
                   happened_on=trial_end_at.date(),
                   happened_at=trial_end_at,
                   subscription_interval=subscription_interval,
                   order_coupon=subscription_coupon)

    orders = sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True)
    for i, order in enumerate(orders):
        if subscription_coupon and i == 0:
            order_coupon = subscription_coupon
        else:
            order_coupon = (order['coupon'] or {}).get('code')

        order_created_at = arrow.get(order['createdAt']).naive
        yield dict(account_id=account_id,
                   type='order',
                   source=f"subscription#{subscription['id']}/order#{i}/created_at",
                   happened_on=order_created_at.date(),
                   happened_at=order_created_at,
                   subscription_interval=subscription['plan']['intervalUnit'],
                   order_coupon=order_coupon)


def classify_referrer(url: str) -> str:
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


def classify_marketing_survey_answer(text: str) -> str:
    if re.search(r'\b(yablk\w+|rob\s*web)\b', text, re.I):
        return 'yablko'
    if re.search(r'\b(pod[ck][aá]st\w*|spotify)\b', text, re.I):
        return 'podcasts'
    if re.search(r'\bpyladies\b', text, re.I):
        return 'pyladies'
    if re.search(r'\bczechitas\b', text, re.I):
        return 'czechitas'
    if re.search(r'\brecenz\w+\b', text, re.I):
        return 'courses_search'
    if (re.search(r'\b(software\s+development\s+academy|sd\s*academy|sda\s+academy)\b', text, re.I) or
        re.search(r'\bSDA\b', text)):
        return 'sdacademy'
    if re.search(r'\b(kurz\w*|akademie|enget\w*|green\s*fox\w*|it\s*network\w*|webin[áa][řr]\w*)\b', text, re.I):
        return 'courses'
    if re.search(r'\b(youtube|yt)\b', text, re.I):
        return 'youtube'
    if re.search(r'\b(facebook\w*|fb|fcb)\b', text, re.I):
        return 'facebook'
    if (re.search(r'\blinkedin\w*\b', text, re.I) or
        re.search(r'\bLI\b', text)):
        return 'linkedin'
    if re.search(r'\b(goo?gl\w*|vyhled[aá]v\w+)\b', text, re.I):
        return 'search'
    if re.search(r'\b(komunit\w+|kamar[aá]d\w*|brat\w*|koleg\w*|br[aá]ch\w*|manžel\w*|partner\w*|p[řr][íi]a?tel\w*|přátelé|pratele|zn[áa]m[ée]\w*|doporu[čc]en\w+)\b', text, re.I):
        return 'friend'
    if re.search(r'^od\s+\w{3,}', text.strip(), re.I):
        return 'friend'
    if re.search(r'\b(\w*hled[aá]\w+|search)\b', text, re.I):
        return 'search'
    return 'other'
