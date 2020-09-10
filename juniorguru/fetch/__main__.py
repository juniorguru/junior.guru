from juniorguru.fetch.fetch_jobs import main as fetch_jobs
from juniorguru.fetch.fetch_logos import main as fetch_logos
from juniorguru.fetch.fetch_metrics import main as fetch_metrics
from juniorguru.fetch.fetch_stories import main as fetch_stories
from juniorguru.fetch.fetch_supporters import main as fetch_supporters
from juniorguru.fetch.fetch_last_modified import main as fetch_last_modified
from juniorguru.fetch.fetch_press_releases import main as fetch_press_releases
from juniorguru.fetch.fetch_newsletter_mentions import main as fetch_newsletter_mentions


def main():
    # order-insensitive
    fetch_stories()
    fetch_supporters()
    fetch_last_modified()
    fetch_press_releases()
    fetch_logos()
    fetch_jobs()

    # order-sensitive
    fetch_metrics()  # depends on jobs & logos
    fetch_newsletter_mentions()  # depends on jobs


if __name__ == '__main__':
    main()
