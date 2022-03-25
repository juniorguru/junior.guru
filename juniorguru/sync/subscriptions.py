from operator import itemgetter
import os
import re

import arrow
from gql import Client as Memberful, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib.tasks import sync_task
from juniorguru.sync import club_content
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


@sync_task(club_content.main)
@db.connection_context()
def main():
    logger.info('Getting data from Memberful')
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463
    transport = RequestsHTTPTransport(url='https://juniorguru.memberful.com/api/graphql/',
                                      headers={'Authorization': f'Bearer {MEMBERFUL_API_KEY}'},
                                      verify=True, retries=3)
    memberful = Memberful(transport=transport)
    query = gql("""
        query getSubscriptions($cursor: String!) {
            subscriptions(after: $cursor) {
                totalCount
                pageInfo {
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
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
    """)

    records = []
    seen_discord_ids = set()

    cursor = ''
    while cursor is not None:
        logger.info('Requesting Memberful GraphQL')
        params = dict(cursor=cursor)
        result = memberful.execute(query, variable_values=params)

        for edge in result['subscriptions']['edges']:
            node = edge['node']
            discord_id = node['member']['discordUserId']
            user = None
            if discord_id:
                seen_discord_ids.add(discord_id)
                try:
                    user = ClubUser.get_by_id(int(discord_id))
                except ClubUser.DoesNotExist:
                    pass

            name = node['member']['fullName'].strip()
            gender = ('F' if FEMALE_NAME_RE.search(name) else 'M') if name else None
            coupon = get_active_coupon(node)
            coupon_parts = parse_coupon(coupon) if coupon else {}

            if node['member']['metadata']:
                print(node['member']['metadata'])

            # TODO
            # sda_student_months = get_student_months(node, 'SDACADEMY')
            # sda_status = get_student_status(node)

            records.append({
                'Name': name,
                'Discord Name': user.display_name.strip() if user else None,
                'Gender': gender,
                'E-mail': node['member']['email'],
                'Memberful ID': node['member']['id'],
                'Stripe ID': node['member']['stripeCustomerId'],
                'Discord ID': discord_id,
                'Invoice ID': coupon_parts.get('invoice_id'),
                'Memberful Active?': node['active'],
                'Memberful Since': arrow.get(node['createdAt']).date().isoformat(),
                'Memberful End': arrow.get(node['expiresAt']).date().isoformat(),
                'Memberful Coupon': coupon,
                'Memberful Coupon Base': coupon_parts.get('coupon_base'),
                'Discord Member?': user.is_member if user else False,
                'Discord Since': user.first_seen_on().isoformat() if user else None,
                'Memberful Past Due?': node['pastDue'],

                # TODO
                # 'SDA Student': ', '.join(sda_student_months),
                # 'SDA Status': None,
            })

            if user:
                logger.debug(f'Updating member #{user.id} with Memberful data')
                joined_memberful_at = arrow.get(node['createdAt']).naive
                user.joined_at = min(user.joined_at, joined_memberful_at) if user.joined_at else joined_memberful_at
                user.coupon_base = coupon_parts.get('coupon_base')
                user.save()

        if result['subscriptions']['pageInfo']['hasNextPage']:
            cursor = result['subscriptions']['pageInfo']['endCursor']
        else:
            cursor = None

    logger.info('Process remaining Discord users')
    for user in ClubUser.listing():
        discord_id = str(user.id)
        if not user.is_bot and discord_id not in seen_discord_ids:
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
            })

    logger.info('Uploading subscriptions to Google Sheets')
    records.sort(key=sort_key, reverse=True)
    if GOOGLE_SHEETS_MUTATIONS_ENABLED:
        google_sheets.upload(google_sheets.get(DOC_KEY, 'subscriptions'), records)
    else:
        logger.warning('Google Sheets mutations not enabled')


def get_active_coupon(node):
    if node['coupon']:
        return node['coupon']['code']

    orders = list(sorted(node['orders'], key=itemgetter('createdAt'), reverse=True))
    try:
        last_order = orders[0]
        if not last_order['coupon']:
            return None
        return last_order['coupon']['code']
    except IndexError:
        return None


def sort_key(record):
    return (
        bool(record['Memberful Active?']),
        bool(record['Discord Member?']),
        bool(record['Memberful ID']),
        record['Discord Since'] if record['Discord Since'] else '2019-01-01',
    )
