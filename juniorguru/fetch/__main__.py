from juniorguru.fetch.jobs import main as fetch_jobs
from juniorguru.fetch.logos import main as fetch_logos
from juniorguru.fetch.metrics import main as fetch_metrics
from juniorguru.fetch.stories import main as fetch_stories
from juniorguru.fetch.supporters import main as fetch_supporters
from juniorguru.fetch.last_modified import main as fetch_last_modified
from juniorguru.fetch.press_releases import main as fetch_press_releases
from juniorguru.fetch.newsletter_mentions import main as fetch_newsletter_mentions
from juniorguru.fetch.transactions import main as fetch_transactions
from juniorguru.fetch.proxies import main as fetch_proxies
from juniorguru.fetch.members import main as fetch_members
from juniorguru.fetch.events import main as fetch_events
from juniorguru.fetch.messages import main as fetch_messages
from juniorguru.fetch.topics import main as fetch_topics
from juniorguru.fetch.roles import main as fetch_roles
from juniorguru.lib.magic import do_magic


def main():
    # order-insensitive
    fetch_stories()
    fetch_supporters()
    fetch_last_modified()
    fetch_press_releases()
    fetch_logos()
    fetch_transactions()
    fetch_proxies()
    fetch_members()
    fetch_messages()

    # order-sensitive
    fetch_events()  # depends on messages
    fetch_topics()  # depends on messages
    fetch_roles()  # depends on messages, events
    fetch_jobs()  # depends on proxies
    fetch_metrics()  # depends on jobs, logos
    fetch_newsletter_mentions()  # depends on jobs

    # cast magic
    do_magic()  # depends on jobs


if __name__ == '__main__':
    main()
