import os

import stripe

from juniorguru.lib.log import get_log


log = get_log('subscriptions')


def main():
    stripe.api_key = os.environ['STRIPE_API_KEY']
    for subscription in stripe.Subscription.list(limit=3):
        print(subscription)


if __name__ == '__main__':
    main()
