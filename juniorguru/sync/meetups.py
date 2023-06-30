from datetime import date
import ics
import re
import click
from playwright.sync_api import sync_playwright
import requests

from juniorguru.cli.sync import default_from_env, main as cli
from juniorguru.lib import loggers


MEETUPCOM_GROUPS = ['reactgirls', 'frontendisti']

ICAL_URLS = {'pyvo': 'https://pyvo.cz/api/pyvo.ics'}


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option('--meetupcom-email', default=default_from_env('MEETUPCOM_EMAIL'))
@click.option('--meetupcom-password', default=default_from_env('MEETUPCOM_PASSWORD'), hide_input=True)
def main(meetupcom_email, meetupcom_password):
    return  # TODO
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

    logger.info('Parsing iCal feeds')
    for ical_slug, ical_text in icals.items():
        logger.info(f'Parsing {ical_slug}')
        calendar = ics.Calendar(ical_text)
        for event in calendar.events:
            if event.begin.date() >= date.today():
                print(event)  # TODO
