import itertools
import math
import re
from datetime import date, datetime, time, timezone
from operator import itemgetter
from pathlib import Path
from typing import Generator
from urllib.parse import urlparse

import arrow
import click
from slugify import slugify

from juniorguru.cli.sync import main as cli
from juniorguru.lib import discord_sync, loggers
from juniorguru.lib.coupons import parse_coupon
from juniorguru.lib.discord_club import ClubClient
from juniorguru.lib.memberful import MemberfulAPI, MemberfulCSV
from juniorguru.models.base import db
from juniorguru.models.feminine_name import FeminineName
from juniorguru.models.partner import Partner
from juniorguru.models.subscription import (SubscriptionActivity,
                                            SubscriptionActivityType,
                                            SubscriptionCancellation,
                                            SubscriptionInternalReferrer,
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
    'thankyou': SubscriptionType.FREE,
    'thankyouforever': SubscriptionType.FREE,
    'thankyouteam': SubscriptionType.FREE,
    'patreon': SubscriptionType.FREE,
    'github': SubscriptionType.FREE,
    'founders': SubscriptionType.FREE,
    'coreskill': SubscriptionType.FREE,
    'studentcoreskill': SubscriptionType.FREE,
    'finaid': SubscriptionType.FINAID,
}

MEMBERS_GQL_PATH = Path(__file__).parent / 'members.gql'


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['partners', 'feminine-names'])
@click.option('--from-date', default='2021-01-01', type=date.fromisoformat)
@click.option('--clear-cache/--keep-cache', default=False)
@click.option('--history-path', default='juniorguru/data/subscription_activities.jsonl', type=click.Path(exists=True, path_type=Path))
@click.option('--clear-history/--keep-history', default=False)
@click.pass_context
@db.connection_context()
def main(context, from_date, clear_cache, history_path, clear_history):
    memberful = MemberfulAPI(cache_dir=context.obj['cache_dir'],
                             clear_cache=clear_cache)

    logger.info('Preparing')
    tables = [SubscriptionActivity,
              SubscriptionReferrer,
              SubscriptionInternalReferrer,
              SubscriptionMarketingSurvey,
              SubscriptionCancellation]
    db.drop_tables(tables)
    db.create_tables(tables)

    subscripton_types_mapping = {
        **{parse_coupon(coupon)['slug']: SubscriptionType.PARTNER
        for coupon in Partner.coupons()},
        **{parse_coupon(coupon)['slug']: SubscriptionType.STUDENT
        for coupon in Partner.student_coupons()},
        **SUBSCRIPTION_TYPES_MAPPING
    }

    # The result of this function will be stored in history, because we cannot store
    # full names of members. If we change how we classify feminine names, there's no
    # way to go back and reclassify the names in the history (without clearing the history).
    def has_feminine_name(name) -> bool:
        return FeminineName.is_feminine(name.strip())

    logger.info('Reading history from a file')
    if clear_history:
        history_path.write_text('')
    else:
        with history_path.open() as f:
            for line in f:
                SubscriptionActivity.deserialize(line)
    from_date = SubscriptionActivity.history_end_on() or from_date

    logger.info(f'Fetching activities from Memberful API, since {from_date}')
    # This heavily relies on history. If there's no history, it will fetch everything
    # since the beginning of time. That's very slow and won't finish, because Memberful API
    # will ban the IP address until the next day. It can be done with cache and different
    # IP addresses (like starting over tethering using LTE of my phone, and re-starting over WiFi).
    queries = (memberful.get_nodes(ACTIVITIES_GQL_PATH.read_text(),
                                   dict(type=type, createdAt=dict(gte=get_timestamp(from_date))))
               for type in ACTIVITY_TYPES_MAPPING)
    for activity in logger.progress(itertools.chain.from_iterable(queries)):
        try:
            account_id = int(activity['member']['id'])
        except (KeyError, TypeError):
            logger.debug('Activity with no account ID, skipping')
        else:
            happened_at = arrow.get(activity['createdAt']).naive
            SubscriptionActivity.add(account_id=account_id,
                                     account_has_feminine_name=has_feminine_name(activity['member']['fullName']),
                                     happened_on=happened_at.date(),
                                     happened_at=happened_at,
                                     type=ACTIVITY_TYPES_MAPPING[activity['type']])
    logger.info(f'Finished with {SubscriptionActivity.total_count()} activities')

    logger.info('Fetching subscriptions from Memberful API')
    # There is no filtering by date, so we need to fetch everything every time. One could
    # say that in such case there's no reason to save the data to history, but the reason
    # we do it is to have a backup (and a git commits to inspect) in case there is something
    # messing with the data again.
    subscriptions = memberful.get_nodes(SUBSCRIPTIONS_GQL_PATH.read_text())
    for subscription in logger.progress(subscriptions):
        for activity in activities_from_subscription(subscription):
            activity['account_has_feminine_name'] = has_feminine_name(subscription['member']['fullName'])
            SubscriptionActivity.add(**activity)
    logger.info(f'Finished with {SubscriptionActivity.total_count()} activities')

    logger.info('Saving history to a file')
    with history_path.open('w') as f:
        for db_object in SubscriptionActivity.history():
            f.write(db_object.serialize())

    logger.info('Classifying subscription types')
    # History only stores coupon slug, so this is done as part of post-processing.
    # It's better than to store the subscription type in the history, because
    # this way over time we can change how the subscription types are classified.
    for activity in SubscriptionActivity.select():
        try:
            activity.subscription_type = subscripton_types_mapping[activity.order_coupon_slug]
        except KeyError:
            activity.subscription_type = SubscriptionType.INDIVIDUAL
        activity.save()

    logger.info('Cleansing data')
    SubscriptionActivity.cleanse_data()

    logger.info('Fetching all members from Memberful API')
    members = list(logger.progress(memberful.get_nodes(MEMBERS_GQL_PATH.read_text())))
    logger.info(f'Got {len(members)} members')
    emails = {member['email']: int(member['id']) for member in members}
    total_spend = {int(member['id']): math.ceil(member['totalSpendCents'] / 100) for member in members}

    logger.info("Fetching members data from Memberful CSV")
    memberful = MemberfulCSV(cache_dir=context.obj['cache_dir'], clear_cache=clear_cache)
    seen_account_ids = set()
    for csv_row in memberful.download_csv(dict(type='MembersCsvExport', filter='all')):
        account_id = int(csv_row['Memberful ID'])
        if account_id in seen_account_ids:
            # This CSV sometimes contains multiple rows for the same account if the account
            # has different plans etc. We do not really care about those fields, so we treat
            # the rows as duplicates to simplify further code.
            continue
        seen_account_ids.add(account_id)

        referrer = csv_row['Referrer'] or None
        if referrer:
            account_details = dict(account_id=account_id,
                                   account_name=csv_row['Full Name'],
                                   account_email=csv_row['Email'],
                                   account_total_spend=total_spend[account_id])
            created_on = date.fromisoformat(csv_row['Created at'])
            referrer_type = classify_referrer(referrer)
            if referrer_type.startswith('/'):
                SubscriptionInternalReferrer.create(created_on=created_on,
                                                    url=referrer,
                                                    path=referrer_type,
                                                    **account_details)
            else:
                SubscriptionReferrer.create(created_on=created_on,
                                            url=referrer,
                                            type=referrer_type,
                                            **account_details)

        marketing_survey_answer = csv_row['Jak ses dozvěděl(a) o junior.guru?'] or None
        if marketing_survey_answer:
            marketing_survey_answer_type = classify_marketing_survey_answer(marketing_survey_answer)
            SubscriptionMarketingSurvey.create(account_id=account_id,
                                               account_name=csv_row['Full Name'],
                                               account_email=csv_row['Email'],
                                               account_total_spend=total_spend[account_id],
                                               created_on=date.fromisoformat(csv_row['Created at']),
                                               value=marketing_survey_answer,
                                               type=marketing_survey_answer_type)

    logger.info("Fetching cancellations data from Memberful CSV")
    csv_rows = itertools.chain(memberful.download_csv(dict(type='CancellationsCsvExport', filter='all')),
                               memberful.download_csv(dict(type='CancellationsCsvExport', scope='completed', filter='all')))
    for csv_row in csv_rows:
        reason = slugify(csv_row['Reason'], separator='_') if csv_row['Reason'] else None
        feedback = csv_row['Feedback'] or None
        if reason:
            try:
                date_field_value = csv_row.get('Date') or csv_row.get('Expiration Date')
                expires_on = date.fromisoformat(date_field_value)
            except ValueError:
                logger.warning(f"Invalid date format: {date_field_value!r}")
                expires_on = None
            account_email = csv_row['Email']
            SubscriptionCancellation.create(account_id=emails[account_email],
                                            account_name=csv_row['Name'],
                                            account_email=account_email,
                                            account_total_spend=total_spend[account_id],
                                            expires_on=expires_on,
                                            reason=reason,
                                            feedback=feedback)

    logger.info("Reporting cancellations")
    discord_sync.run(report_cancellations)


def report_cancellations(client: ClubClient):
    pass


def activities_from_subscription(subscription: dict) -> Generator[dict, None, None]:
    account_id = int(subscription['member']['id'])
    subscription_interval = subscription['plan']['intervalUnit']
    subscription_coupon_slug = get_coupon_slug(subscription['coupon'])

    created_at = arrow.get(subscription['createdAt']).naive
    yield dict(account_id=account_id,
               type='order',
               happened_on=created_at.date(),
               happened_at=created_at,
               subscription_interval=subscription_interval,
               order_coupon_slug=subscription_coupon_slug)
    if subscription['trialStartAt']:
        trial_start_at = arrow.get(subscription['trialStartAt']).naive
        yield dict(account_id=account_id,
                   type='trial_start',
                   happened_on=trial_start_at.date(),
                   happened_at=trial_start_at,
                   subscription_interval=subscription_interval,
                   order_coupon_slug=subscription_coupon_slug)
    if subscription['trialEndAt']:
        trial_end_at = arrow.get(subscription['trialEndAt']).naive
        yield dict(account_id=account_id,
                   type='trial_end',
                   happened_on=trial_end_at.date(),
                   happened_at=trial_end_at,
                   subscription_interval=subscription_interval,
                   order_coupon_slug=subscription_coupon_slug)

    orders = sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True)
    for i, order in enumerate(orders):
        if subscription_coupon_slug and i == 0:
            order_coupon_slug = subscription_coupon_slug
        else:
            order_coupon_slug = get_coupon_slug(order['coupon'])

        order_created_at = arrow.get(order['createdAt']).naive
        yield dict(account_id=account_id,
                   type='order',
                   happened_on=order_created_at.date(),
                   happened_at=order_created_at,
                   subscription_interval=subscription['plan']['intervalUnit'],
                   order_coupon_slug=order_coupon_slug)


def get_timestamp(date: date) -> int:
    return int(datetime.combine(date, time(), tzinfo=timezone.utc).timestamp())


def get_coupon_slug(coupon_data: dict) -> None | str:
    if coupon := (coupon_data or {}).get('code'):
        return parse_coupon(coupon)['slug']
    return None


def classify_referrer(url: str) -> str:
    parts = urlparse(url)
    if parts.netloc == 'junior.guru':
        return parts.path.rstrip('/') or '/'
    if parts.netloc == 't.co':
        return 'twitter'
    if parts.netloc == 'honzajavorek.cz':
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
    if re.search(r'\brecenz\w+\b', text, re.I):
        return 'courses_search'
    if re.search(r'\bpyladies\b', text, re.I):
        return 'courses'
    if re.search(r'\bczechitas\b', text, re.I):
        return 'courses'
    if (re.search(r'\b(software\s+development\s+academy|sd\s*academy|sda\s+academy)\b', text, re.I) or
        re.search(r'\bSDA\b', text)):
        return 'courses'
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
