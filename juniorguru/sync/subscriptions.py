import itertools
from datetime import date, datetime, timedelta
from operator import itemgetter

import arrow

from juniorguru.cli.sync import main as cli
from juniorguru.lib import google_sheets, loggers
from juniorguru.lib.club import parse_coupon
from juniorguru.lib.google_sheets import GOOGLE_SHEETS_MUTATIONS_ENABLED
from juniorguru.lib.memberful import Memberful
from juniorguru.models.base import db
from juniorguru.models.club import (ClubSubscribedPeriod, ClubSubscribedPeriodCategory,
                                    ClubUser)
from juniorguru.models.partner import Partner, PartnerStudentSubscription
from juniorguru.models.feminine_name import FeminineName


logger = loggers.from_path(__file__)


DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'

COUPON_NAMES_CATEGORIES_MAPPING = {
    'THANKYOU': ClubSubscribedPeriodCategory.FREE,
    'THANKYOUFOREVER': ClubSubscribedPeriodCategory.FREE,
    'THANKYOUTEAM': ClubSubscribedPeriodCategory.TEAM,
    'PATREON': ClubSubscribedPeriodCategory.FREE,
    'GITHUB': ClubSubscribedPeriodCategory.FREE,
    'FOUNDERS': ClubSubscribedPeriodCategory.FREE,
    'FINAID': ClubSubscribedPeriodCategory.FINAID,
    'CORESKILL': ClubSubscribedPeriodCategory.CORESKILL,
    'STUDENTCORESKILL': ClubSubscribedPeriodCategory.CORESKILL,
}


@cli.sync_command(dependencies=['club-content',
                                'partners',
                                'feminine-names'])
@db.connection_context()
def main():
    db.drop_tables([PartnerStudentSubscription, ClubSubscribedPeriod])
    db.create_tables([PartnerStudentSubscription, ClubSubscribedPeriod])

    logger.info('Mapping coupons to categories')
    coupon_names_categories_mapping = {
        **{parse_coupon(coupon)['name']: ClubSubscribedPeriodCategory.PARTNER
           for coupon in Partner.coupons()},
        **{parse_coupon(coupon)['name']: ClubSubscribedPeriodCategory.STUDENT
           for coupon in Partner.student_coupons()},
        **COUPON_NAMES_CATEGORIES_MAPPING
    }

    logger.info('Getting data from Memberful')
    memberful = Memberful()
    subscriptions = memberful.get_nodes('subscriptions', """
        id
        active
        createdAt
        expiresAt
        trialStartAt
        trialEndAt
        coupon {
            code
        }
        orders {
            createdAt
            coupon {
                code
            }
        }
        member {
            discordUserId
            email
            fullName
            id
            metadata
        }
        plan {
            intervalUnit
        }
    """)

    records = []
    active_account_ids = set()
    seen_discord_ids = set()
    for subscription in subscriptions:
        account_id = subscription['member']['id']
        if subscription['active']:
            if account_id in active_account_ids:
                logger.warning(f'{account_admin_url(account_id)} has multiple active subscriptions!')
            else:
                active_account_ids.add(account_id)

        discord_id = subscription['member']['discordUserId']
        user = None
        if discord_id:
            seen_discord_ids.add(discord_id)
            try:
                user = ClubUser.get_by_id(int(discord_id))
            except ClubUser.DoesNotExist:
                pass

        name = subscription['member']['fullName'].strip()
        has_feminine_name = FeminineName.is_feminine(name)

        coupon = get_coupon(subscription)
        coupon_parts = parse_coupon(coupon) if coupon else {}
        student_record_fields = dict(itertools.chain.from_iterable([
            [
                (f'{partner.name} Student Since', format_date(get_student_started_on(subscription, partner.student_coupon))),
                (f'{partner.name} Student Months', ', '.join(get_student_months(subscription, partner.student_coupon))),
                (f'{partner.name} Student Invoiced?', subscription['member']['metadata'].get(f'{partner.slug}InvoicedOn'))
            ]
            for partner in Partner.schools_listing()
        ]))

        records.append({
            'Name': name,
            'Discord Name': user.display_name.strip() if user else None,
            'Gender': ('F' if has_feminine_name else 'M'),
            'E-mail': subscription['member']['email'],
            'Memberful': account_admin_url(account_id),
            'Discord ID': discord_id,
            'Memberful Active?': subscription['active'],
            'Memberful Since': arrow.get(subscription['createdAt']).date().isoformat(),
            'Memberful End': arrow.get(subscription['expiresAt']).date().isoformat(),
            'Memberful Coupon': coupon,
            'Memberful Coupon Base': coupon_parts.get('coupon'),
            'Discord Member?': user.is_member if user else False,
            'Discord Since': user.first_seen_on().isoformat() if user else None,
            **student_record_fields,
        })

        for partner in Partner.schools_listing():
            started_on = get_student_started_on(subscription, partner.student_coupon)
            if started_on:
                invoiced_on = subscription['member']['metadata'].get(f'{partner.slug}InvoicedOn')
                invoiced_on = date.fromisoformat(invoiced_on) if invoiced_on else None
                PartnerStudentSubscription.create(partner=partner,
                                                  account_id=account_id,
                                                  name=name,
                                                  email=subscription['member']['email'],
                                                  started_on=started_on,
                                                  invoiced_on=invoiced_on)

        if user:
            logger.debug(f'Updating member #{user.id} with Memberful data')
            # After manual changes to admin some people can have multiple active
            # subscriptions (watch WARNING logs). To save info about the most
            # recent and relevant subscription, the code below checks not only
            # whether the subscription is active, but also whether this particular
            # subscription started later than any other, which might have been
            # already recorded with the user earlier in this loop.
            #
            # TODO: The code will fail to compare three and more subscriptions,
            # because user.subscribed_at will always contain only the earliest date.
            subscribed_at = arrow.get(subscription['createdAt']).naive
            if (
                subscription['active'] and
                (not user.subscribed_at or subscribed_at > user.subscribed_at)
            ):
                user.subscription_id = str(subscription['id'])
                user.coupon = coupon_parts.get('coupon')
            user.update_expires_at(arrow.get(subscription['expiresAt']).naive)
            user.update_subscribed_at(subscribed_at)
            user.has_feminine_name = has_feminine_name
            user.save()

        for subscribed_period in get_subscribed_periods(subscription):
            if subscribed_period['coupon']:
                coupon_name = parse_coupon(subscribed_period['coupon'])['name']
                category = coupon_names_categories_mapping.get(coupon_name, ClubSubscribedPeriodCategory.INDIVIDUALS)
            elif subscribed_period['is_trial']:
                category = ClubSubscribedPeriodCategory.TRIAL
            else:
                category = ClubSubscribedPeriodCategory.INDIVIDUALS
            ClubSubscribedPeriod.create(account_id=account_id,
                                        start_on=subscribed_period['start_on'],
                                        end_on=subscribed_period['end_on'],
                                        interval_unit=subscription['plan']['intervalUnit'],
                                        has_feminine_name=has_feminine_name,
                                        category=category)

    logger.info('Process remaining Discord users')
    for user in ClubUser.members_listing():
        discord_id = str(user.id)
        if not user.is_bot and discord_id not in seen_discord_ids:
            student_record_fields = dict(itertools.chain.from_iterable([
                [
                    (f'{partner.name} Student Since', None),
                    (f'{partner.name} Student Months', None),
                    (f'{partner.name} Student Invoiced?', None)
                ]
                for partner in Partner.schools_listing()
            ]))
            records.append({
                'Name': None,
                'Discord Name': user.display_name.strip(),
                'Gender': None,
                'E-mail': None,
                'Memberful': None,
                'Discord ID': discord_id,
                'Memberful Active?': False,
                'Memberful Since': None,
                'Memberful End': None,
                'Memberful Coupon': None,
                'Memberful Coupon Base': None,
                'Discord Member?': user.is_member,
                'Discord Since': user.first_seen_on().isoformat(),
                **student_record_fields,
            })

    logger.info('Uploading subscriptions to Google Sheets')
    if GOOGLE_SHEETS_MUTATIONS_ENABLED:
        google_sheets.upload(google_sheets.get(DOC_KEY, 'subscriptions'), records)
    else:
        logger.warning('Google Sheets mutations not enabled')


def account_admin_url(account_id):
    return f"https://juniorguru.memberful.com/admin/members/{account_id}"


def format_date(value):
    return f'{value:%Y-%m-%d}' if value else None


def get_coupon(subscription):
    if subscription['coupon']:
        return subscription['coupon']['code']

    orders = list(sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True))
    try:
        last_order = orders[0]
        if not last_order['coupon']:
            return None
        return last_order['coupon']['code']
    except IndexError:
        return None


def get_student_months(subscription, coupon):
    return sorted((f"{datetime.fromtimestamp(order['createdAt']):%Y-%m}"
                   for order in subscription['orders']
                   if (order['coupon'] and
                       order['coupon']['code'].startswith(coupon))))


def get_student_started_on(subscription, coupon):
    orders = (datetime.fromtimestamp(order['createdAt'])
              for order in subscription['orders']
              if (order['coupon'] and
                  order['coupon']['code'].startswith(coupon)))
    try:
        return sorted(orders)[0].date()
    except IndexError:
        return None


def get_subscribed_periods(subscription):
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
