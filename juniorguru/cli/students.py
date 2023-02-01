import csv
import io
import itertools
from datetime import date
from pathlib import Path

import click
from playhouse.shortcuts import model_to_dict

from juniorguru.lib import loggers
from juniorguru.lib.memberful import (MEMBERFUL_MUTATIONS_ENABLED, Memberful,
                                      serialize_metadata)
from juniorguru.models.partner import Partner


logger = loggers.from_path(__file__)


@click.command()
@click.argument('company_slug')
@click.option('--all/--no-all', default=False)
@click.option('--invoice/--no-invoice', default=False)
def main(company_slug, all, invoice):
    if all and invoice:
        logger.error("Can invoice only billable subscriptions, unexpected combination of arguments")
        raise click.Abort()

    try:
        company = Partner.get_by_slug(company_slug)
    except Partner.DoesNotExist:
        slugs = [company.slug for company in Partner.schools_listing()]
        logger.error(f"Partner must be one of: {', '.join(slugs)}")
        raise click.Abort()
    logger.debug(f"Partner identified as {company!r}")

    if all:
        logger.info("All subscriptions")
        subscriptions = list(company.list_student_subscriptions)
    else:
        logger.info("Billable subscriptions")
        subscriptions = list(company.list_student_subscriptions_billable)

    if subscriptions:
        rows = [subscription_to_row(subscription) for subscription in subscriptions]
        csv_content = to_csv(rows)
        print(csv_content.strip())
        path = Path.home() / 'Downloads' / f"{company.slug}-{'all' if all else 'billable'}.csv"
        logger.info(f'Saving to {path}')
        path.write_text(csv_content)
    else:
        logger.warning("Didn't find any subscriptions!")
        return

    if invoice:
        if input('Are you sure you want to mark the above as invoiced? (type YES!) ') != 'YES!':
            logger.error("You're not sure")
            raise click.Abort()

        if not MEMBERFUL_MUTATIONS_ENABLED:
            logger.error('Memberful mutations not enabled')
            raise click.Abort()

        memberful = Memberful()
        query = '''
            query getMembers($cursor: String!) {
                members(after: $cursor) {
                    totalCount
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    edges {
                        node {
                            id
                            metadata
                        }
                    }
                }
            }
        '''
        results = memberful.query(query, lambda result: result['members']['pageInfo'])
        edges = itertools.chain.from_iterable(result['members']['edges']
                                              for result in results)
        members = (edge['node'] for edge in edges)
        members_mapping = {member['id']: member['metadata'] for member in members}

        for subscription in subscriptions:
            logger.info(f'Marking {subscription!r} as invoiced')
            mutation = '''
                mutation ($id: ID!, $metadata: Metadata!) {
                    memberUpdate(id: $id, metadata: $metadata) {
                        member {
                            id
                            metadata
                        }
                    }
                }
            '''
            metadata = members_mapping[subscription.account_id]
            logger.debug(f"Previous metadata: {metadata!r}")
            metadata.setdefault(f'{company.slug}InvoicedOn', date.today().isoformat())
            logger.debug(f"Future metadata: {metadata!r}")
            memberful.mutate(mutation, dict(id=subscription.account_id,
                                            metadata=serialize_metadata(metadata)))


def to_csv(rows):
    if not rows:
        raise ValueError('No rows')
    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return f.getvalue()


def subscription_to_row(subscription):
    return {field_name: value for field_name, value
            in model_to_dict(subscription).items()
            if field_name in ['name', 'email', 'started_on', 'invoiced_on']}
