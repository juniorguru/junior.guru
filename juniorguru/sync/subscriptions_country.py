import click
import stripe

from juniorguru.cli.sync import default_from_env, main as cli
from juniorguru.lib import loggers
from juniorguru.models.subscription import SubscriptionCountry


logger = loggers.from_path(__file__)


# https://stripe.com/guides/introduction-to-eu-vat-and-vat-oss#3-gather-evidence-of-buyer-location
# https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/declare-and-pay-oss_en


@cli.sync_command()
@click.option("--stripe-api-key", default=default_from_env("STRIPE_API_KEY"))
def main(stripe_api_key: str):
    SubscriptionCountry.drop_table()
    SubscriptionCountry.create_table()

    customers = stripe.Customer.list(api_key=stripe_api_key)
    for customer in logger.progress(customers.auto_paging_iter()):
        payment_methods = customer.list_payment_methods(type="card", limit=1)
        try:
            country_code = payment_methods.data[0].card.country
        except IndexError:
            logger.debug(f"Customer {customer.id} ({customer.email}) has no card")
        else:
            SubscriptionCountry.create(customer_id=customer.id, country_code=country_code)
