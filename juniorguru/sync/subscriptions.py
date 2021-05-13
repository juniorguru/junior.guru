import os

from gql import Client as Memberful, gql
from gql.transport.requests import RequestsHTTPTransport
# import stripe

from juniorguru.lib.log import get_log


log = get_log('subscriptions')


def main():
    # stripe.api_key = os.environ['STRIPE_API_KEY']
    # for subscription in stripe.Subscription.list().auto_paging_iter():
    #     print(subscription['metadata'])

    # https://memberful.com/help/integrate/advanced/memberful-api/
    # https://juniorguru.memberful.com/api/graphql/explorer

    api_key = os.environ['MEMBERFUL_API_KEY']
    transport = RequestsHTTPTransport(url='https://juniorguru.memberful.com/api/graphql/',
                                      headers={'Authorization': f'Bearer {api_key}'},
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
                            state
                        }
                        member {
                            discordUserId
                            email
                            fullName
                            id
                            stripeCustomerId
                            username
                        }
                    }
                }
            }
        }
    """)
    params = dict(cursor='')
    result = memberful.execute(query, params)
    from pprint import pprint; pprint(result)


if __name__ == '__main__':
    main()
