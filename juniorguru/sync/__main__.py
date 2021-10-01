import sys
import importlib

from juniorguru.lib.log import get_log
from juniorguru.lib import timer
from juniorguru.sync.employments import main as sync_employments
from juniorguru.sync.jobs import main as sync_jobs
from juniorguru.sync.logos import main as sync_logos
from juniorguru.sync.metrics import main as sync_metrics
from juniorguru.sync.stories import main as sync_stories
from juniorguru.sync.supporters import main as sync_supporters
from juniorguru.sync.last_modified import main as sync_last_modified
from juniorguru.sync.press_releases import main as sync_press_releases
from juniorguru.sync.transactions import main as sync_transactions
from juniorguru.sync.proxies import main as sync_proxies
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
from juniorguru.sync.jobs_club import main as sync_jobs_club
from juniorguru.lib.ai import set_ai_opinion


log = get_log('sync')


@timer.notify
@timer.measure('sync')
def main():
    # order-insensitive
    sync_stories()
    sync_supporters()
    sync_last_modified()
    sync_press_releases()
    sync_logos()
    sync_companies()  # might depend on subscriptions one day?
    sync_transactions()
    sync_proxies()
    sync_club_content()
    sync_employments()

    # order-sensitive
    sync_mentoring()  # depends on club_content
    sync_pins()  # depends on club_content
    sync_avatars()  # depends on club_content
    sync_events()  # depends on club_content
    sync_topics()  # depends on club_content
    sync_digest()  # depends on club_content
    sync_returning_members()  # depends on club_content
    sync_subscriptions()  # depends on club_content
    sync_roles()  # depends on club_content, events, avatars, subscriptions
    sync_jobs()  # depends on proxies, employments
    sync_metrics()  # depends on jobs, logos, transactions
    set_ai_opinion()  # depends on employments
    sync_jobs_club()  # depends on employments, jobs, club_content (in the future: set_ai_opinion)


try:
    module_name = f'juniorguru.sync.{sys.argv[1]}'.replace('-', '_')
except IndexError:
    # Standard `make sync`, i.e. `poetry run python -m juniorguru.sync`
    main()
else:
    # For debugging purposes, one can run `make sync SYNC=stories`,
    # which is a shortcut for `poetry run python -m juniorguru.sync stories`,
    # which is a shortcut for `poetry run python -m juniorguru.sync.stories`
    log.info(f"Running only: {module_name}")
    module = importlib.import_module(module_name)
    timer.notify(module.main)()
log.info('Synchronization done!')
