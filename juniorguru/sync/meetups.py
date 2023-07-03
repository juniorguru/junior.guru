from functools import partial
import json
import re
from datetime import date

import click
import ics
import requests
from playwright.sync_api import sync_playwright

from juniorguru.cli.sync import default_from_env, main as cli
from juniorguru.lib import loggers


MEETUPCOM_GROUPS = ['reactgirls', 'frontendisti']

ICAL_URLS = {'pyvo': 'https://pyvo.cz/api/pyvo.ics'}


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--meetupcom-email', default=default_from_env('MEETUPCOM_EMAIL'))
@click.option('--meetupcom-password', default=default_from_env('MEETUPCOM_PASSWORD'), hide_input=True)
@click.pass_context
def main(context, meetupcom_email, meetupcom_password):
    logger.info('Reading cache')
    cache_path = context.obj['cache_dir'] / 'meetups.json'
    try:
        icals = json.loads(cache_path.read_text())
    except FileNotFoundError:
        logger.warning('No cache found')
        icals = {}

        logger.info('About to scrape meetup.com (use PWDEBUG=1 to debug this)')
        with sync_playwright() as playwright:
            browser = playwright.firefox.launch()
            page = browser.new_page()

            logger.info('Logging into meetup.com')
            page.goto('https://www.meetup.com/login/', wait_until='networkidle')
            page.fill('#email', meetupcom_email)
            page.fill('#current-password', meetupcom_password)
            page.click('button[data-event-label="login-with-email"]')
            page.wait_for_url(re.compile(r'meetup\.com/home'), wait_until='domcontentloaded')

            for group in MEETUPCOM_GROUPS:
                group_url = f'https://www.meetup.com/{group}/events/calendar/'
                logger.info(f'Going to {group_url}')
                page.goto(f'https://www.meetup.com/{group}/events/calendar/', wait_until='networkidle')

                logger.info("Downloading iCal (an open format they've decided to put behind a login wall)")
                with page.expect_download() as download_info:
                    page.click('a[href*="/ical/"]')
                download = download_info.value
                icals[group] = download.path().read_text()
                logger.info('Success!')

        logger.info('About to download other iCal feeds')
        for ical_slug, ical_url in ICAL_URLS.items():
            logger.info(f'Downloading {ical_url}')
            response = requests.get(ical_url, headers={'User-Agent': 'JuniorGuruBot (+https://junior.guru)'})
            response.raise_for_status()
            icals[ical_slug] = response.text.strip()

    logger.info('Caching iCal feeds')
    cache_path.write_text(json.dumps(icals, ensure_ascii=False, indent=2, sort_keys=True))

    logger.info('Parsing iCal feeds')
    for ical_slug, ical_text in icals.items():
        logger.info(f'Parsing {ical_slug}')
        calendar = ics.Calendar(ical_text)
        for event in filter(partial(is_future_event, today=date.today()), calendar.events):
            print(event)


def is_future_event(event: ics.Event, today: date) -> bool:
    return (event.begin.date() >= today
            and 'tentative-date' not in event.categories)
