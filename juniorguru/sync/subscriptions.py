from operator import itemgetter
import os

import arrow
from gql import Client as Memberful, gql
from gql.transport.requests import RequestsHTTPTransport

from juniorguru.lib.log import get_log
from juniorguru.lib import google_sheets
from juniorguru.models import ClubUser


log = get_log('subscriptions')


MEMBERFUL_API_KEY = os.environ['MEMBERFUL_API_KEY']
DOC_KEY = '1TO5Yzk0-4V_RzRK5Jr9I_pF5knZsEZrNn2HKTXrHgls'


def main():
    log.info('Getting data from Memberful')
    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer?api_user_id=52463
    transport = RequestsHTTPTransport(url='https://juniorguru.memberful.com/api/graphql/',
                                      headers={'Authorization': f'Bearer {MEMBERFUL_API_KEY}'},
                                      verify=True, retries=3)
    memberful = Memberful(transport=transport, fetch_schema_from_transport=True)
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
        log.info('Requesting Memberful GraphQL')
        params = dict(cursor=cursor)
        result = memberful.execute(query, params)

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

            records.append({
                'Name': node['member']['fullName'],
                'Discord Name': user.display_name if user else None,
                'E-mail': node['member']['email'],
                'Memberful ID': node['member']['id'],
                'Stripe ID': node['member']['stripeCustomerId'],
                'Discord ID': discord_id,
                'Memberful Active?': node['active'],
                'Memberful Since': arrow.get(node['createdAt']).date().isoformat(),
                'Memberful End': arrow.get(node['expiresAt']).date().isoformat(),
                'Memberful Coupon': get_active_coupon(node),
                'Discord Member?': user.is_member if user else False,
                'Discord Since': user.first_seen_on().isoformat() if user else None,
                'Memberful Past Due?': node['pastDue'],
            })

        if result['subscriptions']['pageInfo']['hasNextPage']:
            cursor = result['subscriptions']['pageInfo']['endCursor']
        else:
            cursor = None

    log.info('Process remaining Discord users')
    for user in ClubUser.listing():
        discord_id = str(user.id)
        if not user.is_bot and discord_id not in seen_discord_ids:
            records.append({
                'Name': None,
                'Discord Name': user.display_name,
                'E-mail': None,
                'Memberful ID': None,
                'Stripe ID': None,
                'Discord ID': discord_id,
                'Memberful Active?': False,
                'Memberful Since': None,
                'Memberful End': None,
                'Memberful Coupon': None,
                'Discord Member?': user.is_member,
                'Discord Since': user.first_seen_on().isoformat(),
                'Memberful Past Due?': False,
            })

    log.info('Uploading subscriptions to Google Sheets')
    google_sheets.upload(google_sheets.get(DOC_KEY, 'subscriptions'), records)


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


if __name__ == '__main__':
    main()
