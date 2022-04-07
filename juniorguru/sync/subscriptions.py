from operator import itemgetter
from datetime import datetime, date
import itertools
import os
import re

import arrow

from juniorguru.lib.memberful import Memberful
from juniorguru.lib.tasks import sync_task
from juniorguru.models import Company, CompanyStudentSubscription
from juniorguru.sync.club_content import main as club_content_task
from juniorguru.sync.companies import main as companies_task
from juniorguru.lib import loggers
from juniorguru.lib import google_sheets
from juniorguru.lib.google_sheets import GOOGLE_SHEETS_MUTATIONS_ENABLED
from juniorguru.models import ClubUser, db
from juniorguru.lib.club import parse_coupon


logger = loggers.get(__name__)


MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']

DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'

FEMALE_NAME_RE = re.compile(r'''
    (\w+\s\w+ov[aá]$)|
    (\w+\s\w+ská$)|
    (\b(
        Jana|Marie|Eva|Hana|Anna|Lenka|Kate[řr]ina|Lucie|V[eě]ra|Alena|Petra|Veronika|Jaroslava|
        Tereza|Martina|Michaela|Jitka|Helena|Ludmila|Zde[ňn]ka|Ivana|Monika|Eli[šs]ka|Zuzana|
        Mark[ée]ta|Jarmila|Barbora|Ji[řr]ina|Marcela|Krist[ýy]na|Alexandra|Daniela|Kayla|
        Hann?ah?|Mia|Kl[áa]ra|Olga|Nath?[áa]lie|Adina|Karol[íi]na|Ane[žz]ka|Marij?[ea]|Alisa|
        Hany|Dominika|Marta|Nikola
    )\b)
''', re.VERBOSE | re.IGNORECASE)


@sync_task(club_content_task, companies_task)
@db.connection_context()
def main():
    CompanyStudentSubscription.drop_table()
    CompanyStudentSubscription.create_table()

    logger.info('Getting data from Memberful')
    memberful = Memberful()
    query = """
        query getSubscriptions($cursor: String!) {
            subscriptions(after: $cursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        id
                        active
                        createdAt
                        expiresAt
                        pastDue
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
                            stripeCustomerId
                        }
                    }
                }
            }
        }
    """

    records = []
    seen_discord_ids = set()
    for result in memberful.query(query, lambda result: result['subscriptions']['pageInfo']):
        for edge in result['subscriptions']['edges']:
            subscription = edge['node']
            discord_id = subscription['member']['discordUserId']
            user = None
            if discord_id:
                seen_discord_ids.add(discord_id)
                try:
                    user = ClubUser.get_by_id(int(discord_id))
                except ClubUser.DoesNotExist:
                    pass

            name = subscription['member']['fullName'].strip()
            gender = ('F' if FEMALE_NAME_RE.search(name) else 'M') if name else None
            coupon = get_active_coupon(subscription)
            coupon_parts = parse_coupon(coupon) if coupon else {}
            student_record_fields = dict(itertools.chain.from_iterable([
                [
                    (f'{company.name} Student Since', format_date(get_student_started_on(subscription, company.student_coupon_base))),
                    (f'{company.name} Student Months', ', '.join(get_student_months(subscription, company.student_coupon_base))),
                    (f'{company.name} Student Invoiced?', subscription['member']['metadata'].get(f'{company.slug}InvoicedOn'))
                ]
                for company in Company.schools_listing()
            ]))

            records.append({
                'Name': name,
                'Discord Name': user.display_name.strip() if user else None,
                'Gender': gender,
                'E-mail': subscription['member']['email'],
                'Memberful ID': subscription['member']['id'],
                'Stripe ID': subscription['member']['stripeCustomerId'],
                'Discord ID': discord_id,
                'Invoice ID': coupon_parts.get('invoice_id'),
                'Memberful Active?': subscription['active'],
                'Memberful Since': arrow.get(subscription['createdAt']).date().isoformat(),
                'Memberful End': arrow.get(subscription['expiresAt']).date().isoformat(),
                'Memberful Coupon': coupon,
                'Memberful Coupon Base': coupon_parts.get('coupon_base'),
                'Discord Member?': user.is_member if user else False,
                'Discord Since': user.first_seen_on().isoformat() if user else None,
                'Memberful Past Due?': subscription['pastDue'],
                **student_record_fields,
            })

            for company in Company.schools_listing():
                started_on = get_student_started_on(subscription, company.student_coupon_base)
                if started_on:
                    invoiced_on = subscription['member']['metadata'].get(f'{company.slug}InvoicedOn')
                    invoiced_on = date.fromisoformat(invoiced_on) if invoiced_on else None
                    CompanyStudentSubscription.create(company=company,
                                                      memberful_id=subscription['member']['id'],
                                                      name=name,
                                                      email=subscription['member']['email'],
                                                      started_on=started_on,
                                                      invoiced_on=invoiced_on)

            if user:
                logger.debug(f'Updating member #{user.id} with Memberful data')
                joined_memberful_at = arrow.get(subscription['createdAt']).naive
                user.subscription_id = str(subscription['id'])
                user.joined_at = min(user.joined_at, joined_memberful_at) if user.joined_at else joined_memberful_at
                user.expires_at = arrow.get(subscription['expiresAt']).naive
                user.coupon_base = coupon_parts.get('coupon_base')
                user.save()

    logger.info('Process remaining Discord users')
    for user in ClubUser.listing():
        discord_id = str(user.id)
        if not user.is_bot and discord_id not in seen_discord_ids:
            student_record_fields = dict(itertools.chain.from_iterable([
                [
                    (f'{company.name} Student Since', None),
                    (f'{company.name} Student Months', None),
                    (f'{company.name} Student Invoiced?', None)
                ]
                for company in Company.schools_listing()
            ]))
            records.append({
                'Name': None,
                'Discord Name': user.display_name.strip(),
                'Gender': None,
                'E-mail': None,
                'Memberful ID': None,
                'Stripe ID': None,
                'Discord ID': discord_id,
                'Invoice ID': None,
                'Memberful Active?': False,
                'Memberful Since': None,
                'Memberful End': None,
                'Memberful Coupon': None,
                'Memberful Coupon Base': None,
                'Discord Member?': user.is_member,
                'Discord Since': user.first_seen_on().isoformat(),
                'Memberful Past Due?': False,
                **student_record_fields,
            })

    logger.info('Uploading subscriptions to Google Sheets')
    if GOOGLE_SHEETS_MUTATIONS_ENABLED:
        google_sheets.upload(google_sheets.get(DOC_KEY, 'subscriptions'), records)
    else:
        logger.warning('Google Sheets mutations not enabled')


def format_date(value):
    return f'{value:%Y-%m-%d}' if value else None


def get_active_coupon(subscription):
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


def get_student_months(subscription, coupon_base):
    return sorted((f"{datetime.fromtimestamp(order['createdAt']):%Y-%m}"
                   for order in subscription['orders']
                   if (order['coupon'] and
                       order['coupon']['code'].startswith(coupon_base))))


def get_student_started_on(subscription, coupon_base):
    orders = (datetime.fromtimestamp(order['createdAt'])
              for order in subscription['orders']
              if (order['coupon'] and
                  order['coupon']['code'].startswith(coupon_base)))
    try:
        return sorted(orders)[0].date()
    except IndexError:
        return None
