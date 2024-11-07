import itertools
from datetime import date, datetime, time, timedelta, timezone

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers, mutations
from jg.coop.lib.memberful import MemberfulAPI
from jg.coop.models.base import db
from jg.coop.models.partner import Partner
from jg.coop.models.sponsor import Sponsor


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["organizations"])
@db.connection_context()
def main():
    today = date.today()
    memberful = MemberfulAPI()
    mutation = """
        mutation ($id: ID!, $expiresAt: Int!) {
            subscriptionChangeExpirationTime(id: $id, expiresAt: $expiresAt) {
                subscription {
                    id
                    expiresAt
                }
            }
        }
    """
    for org in itertools.chain(Sponsor.listing(), Partner.free_listing()):
        if org.subscription_id:
            renews_on = getattr(org, "renews_on", today + timedelta(days=365))
            logger.info(f"Organization {org.slug!r} renews on {renews_on}")
            renews_at = datetime.combine(renews_on, time(tzinfo=timezone.utc))
            params = dict(id=org.subscription_id, expiresAt=int(renews_at.timestamp()))
            logger.debug(f"Updating organization {org.slug!r} to renew at {renews_at}")
            if align_subscription(memberful, mutation, params):
                logger.info(
                    f"{org.slug!r} subscription updated to expire at {renews_at}"
                )
        else:
            logger.info(f"Organization {org.slug!r} has no subscription")


@mutations.mutates_memberful()
def align_subscription(memberful, mutation, params):
    return memberful.mutate(mutation, params)
