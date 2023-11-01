from concurrent.futures import ThreadPoolExecutor, as_completed

import click
import stripe

from juniorguru.cli.sync import Cache, default_from_env, main as cli
from juniorguru.lib import loggers
from juniorguru.models.subscription import SubscriptionCountry


WORKERS = 10


logger = loggers.from_path(__file__)


# https://stripe.com/guides/introduction-to-eu-vat-and-vat-oss#3-gather-evidence-of-buyer-location
# https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en


@cli.sync_command()
@cli.pass_cache
@click.option("--clear-cache/--keep-cache", default=False)
@click.option("--stripe-api-key", default=default_from_env("STRIPE_API_KEY"))
def main(cache: Cache, clear_cache: bool, stripe_api_key: str):
    if clear_cache:
        cache.delete("subscriptions_country")

    SubscriptionCountry.drop_table()
    SubscriptionCountry.create_table()

    try:
        records = cache["subscriptions_country"]
        logger.info("Loading from cache")
    except KeyError:
        customers = stripe.Customer.list(api_key=stripe_api_key)
        customers = logger.progress(customers.auto_paging_iter())

        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            threads = [executor.submit(get_data, customer) for customer in customers]
        records = [thread.result() for thread in as_completed(threads)]
        cache["subscriptions_country"] = records

    for record in records:
        if record["country_code"]:
            SubscriptionCountry.create(**record)
        else:
            logger.debug(
                f"Customer {record['customer_id']} ({record['customer_email']}) has no card"
            )


def get_data(customer: stripe.Customer) -> str:
    payment_methods = customer.list_payment_methods(type="card", limit=1)
    try:
        country_code = payment_methods.data[0].card.country
    except IndexError:
        country_code = None
    return dict(
        customer_id=customer.id,
        customer_email=customer.email,
        country_code=country_code,
    )
