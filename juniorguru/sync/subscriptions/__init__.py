import itertools
from pathlib import Path

import arrow

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.memberful import Memberful
from juniorguru.models.base import db
from juniorguru.models.club import (ClubSubscriptionActivity,
                                    ClubSubscriptionActivityType)


ACTIVITIES_GQL_PATH = Path(__file__).parent / 'activities.gql'

ACTIVITY_TYPES_MAPPING = {
    'new_order': ClubSubscriptionActivityType.BEGIN,
    'new_gift': ClubSubscriptionActivityType.BEGIN,
    'subscription_deleted': ClubSubscriptionActivityType.END,
    'member_deleted': ClubSubscriptionActivityType.END,
    'subscription_deactivated': ClubSubscriptionActivityType.END,
}


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    ClubSubscriptionActivity.drop_table()
    ClubSubscriptionActivity.create_table()

    memberful = Memberful()
    logger.info('Getting new orders from Memberful')
    query = ACTIVITIES_GQL_PATH.read_text()
    activities = itertools.chain(memberful.get_nodes(query, dict(type='new_order')),
                                 memberful.get_nodes(query, dict(type='new_gift')),
                                 memberful.get_nodes(query, dict(type='subscription_deleted')),
                                 memberful.get_nodes(query, dict(type='member_deleted')),
                                 memberful.get_nodes(query, dict(type='subscription_deactivated')))
    for activity in activities:
        try:
            account_id = activity['member']['id']
        except (KeyError, TypeError):
            account_id = None
        activity_type = ACTIVITY_TYPES_MAPPING[activity['type']]
        happening_on = arrow.get(activity['createdAt']).date()
        logger.info(f"Saving {activity_type.upper()} activity for account {format_account_id(account_id)}, {happening_on}")
        ClubSubscriptionActivity.create(account_id=account_id,
                                        happening_on=happening_on,
                                        type=activity_type)
    count = ClubSubscriptionActivity.delete_duplicates()
    logger.info(f"Deleted {count} duplicates")


def format_account_id(account_id):
    return f"#{account_id}" if account_id else '(deleted account)'
