from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

import click
import stripe

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cache import cache
from jg.coop.models.base import db
from jg.coop.models.subscription import SubscriptionCountry


WORKERS = 10


logger = loggers.from_path(__file__)


# https://stripe.com/guides/introduction-to-eu-vat-and-vat-oss#3-gather-evidence-of-buyer-location
# https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en


@cli.sync_command()
@click.option("--stripe-api-key", default=default_from_env("STRIPE_API_KEY"))
@db.connection_context()
def main(stripe_api_key: str):
    SubscriptionCountry.drop_table()
    SubscriptionCountry.create_table()

    for customer in fetch_customers(stripe_api_key):
        if customer["country_code"]:
            SubscriptionCountry.create(
                customer_id=customer["id"],
                customer_email=customer["email"],
                country_code=customer["country_code"],
            )
        else:
            logger.debug(f"Customer {customer['id']} ({customer['email']}) has no card")


@cache(expire=timedelta(days=30), tag="stripe-customers")
def fetch_customers(stripe_api_key: str) -> list[str]:
    customers = stripe.Customer.list(api_key=stripe_api_key)
    customers = logger.progress(customers.auto_paging_iter())

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        threads = [
            executor.submit(fetch_customer_data, customer) for customer in customers
        ]
        return [thread.result() for thread in as_completed(threads)]


def fetch_customer_data(customer: stripe.Customer) -> str:
    payment_methods = customer.list_payment_methods(type="card", limit=1)
    try:
        country_code = payment_methods.data[0].card.country
    except IndexError:
        country_code = None
    return dict(
        id=customer.id,
        email=customer.email,
        country_code=country_code,
    )
