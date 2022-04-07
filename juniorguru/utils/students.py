import csv
import io
import itertools
from datetime import date
from pathlib import Path

from invoke import Exit, task
from playhouse.shortcuts import model_to_dict

from juniorguru.lib import loggers
from juniorguru.lib.memberful import (MEMBERFUL_MUTATIONS_ENABLED, Memberful,
                                      serialize_metadata)
from juniorguru.models.company import Company


logger = loggers.get(__name__)


@task(name='students')
def main(context, company_slug, all=False, invoice=False):
    if all and invoice:
        logger.error("Can invoice only billable subscriptions, unexpected combination of arguments")
        raise Exit(code=1)

    try:
        company = Company.get_by_slug(company_slug)
    except Company.DoesNotExist:
        slugs = [company.slug for company in Company.schools_listing()]
        logger.error(f"Company must be one of: {', '.join(slugs)}")
        raise Exit(code=1)
    logger.debug(f"Company identified as {company!r}")

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
        raise Exit(code=0)

    if invoice:
        if input('Are you sure you want to mark the above as invoiced? (type YES!) ') != 'YES!':
            logger.error("You're not sure")
            raise Exit(code=1)

        if not MEMBERFUL_MUTATIONS_ENABLED:
            logger.error('Memberful mutations not enabled')
            raise Exit(code=1)

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
            metadata = members_mapping[subscription.memberful_id]
            logger.debug(f"Previous metadata: {metadata!r}")
            metadata.setdefault(f'{company.slug}InvoicedOn', date.today().isoformat())
            logger.debug(f"Future metadata: {metadata!r}")
            memberful.mutate(mutation, dict(id=subscription.memberful_id,
                                            metadata=serialize_metadata(metadata)))


def to_csv(rows):
    f = io.StringIO()
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return f.getvalue()


def subscription_to_row(subscription):
    return {field_name: value for field_name, value
            in model_to_dict(subscription).items()
            if field_name in ['name', 'email', 'started_on', 'invoiced_on']}
