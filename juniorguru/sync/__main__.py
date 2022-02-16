import sys
import importlib

from juniorguru.lib import loggers
from juniorguru.lib import timer
# from juniorguru.sync.metrics import main as sync_metrics
from juniorguru.sync.stories import main as sync_stories
from juniorguru.sync.supporters import main as sync_supporters
from juniorguru.sync.last_modified import main as sync_last_modified
from juniorguru.sync.transactions import main as sync_transactions
from juniorguru.sync.events import main as sync_events
from juniorguru.sync.club_content import main as sync_club_content
from juniorguru.sync.topics import main as sync_topics
from juniorguru.sync.roles import main as sync_roles
from juniorguru.sync.avatars import main as sync_avatars
from juniorguru.sync.returning_members import main as sync_returning_members
from juniorguru.sync.digest import main as sync_digest
from juniorguru.sync.pins import main as sync_pins
from juniorguru.sync.subscriptions import main as sync_subscriptions
from juniorguru.sync.companies import main as sync_companies
from juniorguru.sync.mentoring import main as sync_mentoring
from juniorguru.sync.li_group import main as sync_li_group
# from juniorguru.sync.jobs_club import main as sync_jobs_club
from juniorguru.sync.stickers import main as sync_stickers
from juniorguru.sync.podcast import main as sync_podcast
from juniorguru.sync.jobs_scraped import main as sync_jobs_scraped
from juniorguru.sync.jobs_submitted import main as sync_jobs_submitted
# from juniorguru.lib.ai import set_ai_opinion


logger = loggers.get('juniorguru.sync')


@timer.notify
@timer.measure('sync')
def main():
    # order-insensitive
    sync_stories()
    sync_supporters()
    sync_last_modified()
    sync_companies()
    sync_transactions()
    sync_club_content()
    sync_podcast()
    sync_jobs_scraped()
    sync_jobs_submitted()

    # depends on club_content
    sync_stickers()
    sync_mentoring()
    sync_li_group()
    sync_pins()
    sync_avatars()
    sync_events()
    sync_topics()
    sync_digest()
    sync_returning_members()
    sync_subscriptions()

    # order-sensitive
    sync_roles()  # depends on club_content, events, avatars, subscriptions, companies
    # TODO sync_metrics()  # depends on jobs, logos, transactions
    # TODO set_ai_opinion()  # depends on employments
    # TODO sync_jobs_club()  # depends on employments, jobs, club_content (in the future: set_ai_opinion)


try:
    module_name = f'juniorguru.sync.{sys.argv[1]}'.replace('-', '_')
except IndexError:
    # Standard `make sync`, i.e. `poetry run python -m juniorguru.sync`
    main()
else:
    # For debugging purposes, one can run `make sync SYNC=stories`,
    # which is a shortcut for `poetry run python -m juniorguru.sync stories`,
    # which is a shortcut for `poetry run python -m juniorguru.sync.stories`
    logger.info(f"Running only: {module_name}")
    module = importlib.import_module(module_name)
    timer.notify(module.main)()
logger.info('Synchronization done!')
