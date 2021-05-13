import sys
import importlib

from juniorguru.lib.log import get_log
from juniorguru.sync.jobs import main as sync_jobs, manage_jobs_voting_channel
from juniorguru.sync.logos import main as sync_logos
from juniorguru.sync.metrics import main as sync_metrics
from juniorguru.sync.stories import main as sync_stories
from juniorguru.sync.supporters import main as sync_supporters
from juniorguru.sync.last_modified import main as sync_last_modified
from juniorguru.sync.press_releases import main as sync_press_releases
from juniorguru.sync.newsletter_mentions import main as sync_newsletter_mentions
from juniorguru.sync.transactions import main as sync_transactions
from juniorguru.sync.proxies import main as sync_proxies
from juniorguru.sync.members import main as sync_members
from juniorguru.sync.events import main as sync_events
from juniorguru.sync.messages import main as sync_messages
from juniorguru.sync.topics import main as sync_topics
from juniorguru.sync.roles import main as sync_roles
from juniorguru.lib.magic import do_magic


log = get_log('sync')


def main():
    # order-insensitive
    sync_stories()
    sync_supporters()
    sync_last_modified()
    sync_press_releases()
    sync_logos()
    sync_transactions()
    sync_proxies()
    sync_members()
    sync_messages()

    # order-sensitive
    sync_events()  # depends on messages
    sync_topics()  # depends on messages
    sync_roles()  # depends on messages, events
    sync_jobs()  # depends on proxies
    sync_metrics()  # depends on jobs, logos
    sync_newsletter_mentions()  # depends on jobs

    # cast magic
    do_magic()  # depends on jobs
    manage_jobs_voting_channel()  # depends on magic


if __name__ == '__main__':
    try:
        module_name = f'juniorguru.sync.{sys.argv[1]}'
    except IndexError:
        # Standard `pipenv run sync`, i.e. `pipenv run python -m juniorguru.sync`
        main()
    else:
        # For debugging purposes, one can run `pipenv run sync stories`,
        # which is a shortcut for `pipenv run python -m juniorguru.sync.stories`
        log.info(f"Running only: {module_name}")
        module = importlib.import_module(module_name)
        module.main()
    log.info('Synchronization done!')
