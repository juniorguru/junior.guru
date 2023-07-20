import itertools
import click

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.memberful import MemberfulCSV
from juniorguru.models.base import db
from juniorguru.models.subscription import SubscriptionCancellation, SubscriptionOrigin, SubscriptionReferrer


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--clear-cache/--keep-cache', default=False)
@click.pass_context
@db.connection_context()
def main(context, clear_cache):
    logger.info("Preparing database")
    tables = [SubscriptionReferrer, SubscriptionOrigin, SubscriptionCancellation]
    db.drop_tables(tables)
    db.create_tables(tables)

    logger.info("Fetching members data from Memberful")
    memberful = MemberfulCSV(cache_dir=context.obj['cache_dir'], clear_cache=clear_cache)
    for csv_row in memberful.download_csv(dict(type='MembersCsvExport', filter='all')):
        referrer = csv_row['Referrer'] or None
        if referrer:
            SubscriptionReferrer.create(account_id=csv_row['Memberful ID'],
                                        name=csv_row['Full Name'],
                                        email=csv_row['Email'],
                                        referrer=referrer)
        origin = csv_row['Jak ses dozvěděl(a) o junior.guru?'] or None
        if origin:
            SubscriptionOrigin.create(account_id=csv_row['Memberful ID'],
                                      name=csv_row['Full Name'],
                                      email=csv_row['Email'],
                                      origin=origin)

    logger.info("Fetching cancellations data from Memberful")
    csv_rows = itertools.chain(memberful.download_csv(dict(type='CancellationsCsvExport', filter='all')),
                               memberful.download_csv(dict(type='CancellationsCsvExport', scope='completed', filter='all')))
    for csv_row in csv_rows:
        reason = csv_row['Reason'] or None
        feedback = csv_row['Feedback'] or None
        if reason:
            SubscriptionCancellation.create(name=csv_row['Name'],
                                            email=csv_row['Email'],
                                            reason=reason,
                                            feedback=feedback)
