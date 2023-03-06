import json
import re
from datetime import date
from pathlib import Path

import click
import requests
from lxml import html
from playwright.sync_api import sync_playwright

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


YOUTUBE_URL = 'https://www.youtube.com/@juniordotguru'

YOUTUBE_CONSENT_FORM_URL = 'https://consent.youtube.com/save'

YOUTUBE_LANGUAGE_FORM_URL = 'https://consent.youtube.com/ml'

LINKEDIN_URL = 'https://www.linkedin.com/company/juniorguru'

LINKEDIN_PERSONAL_URL = 'https://www.linkedin.com/posts/honzajavorek_courting-haskell-honza-javorek-activity-6625070791035756544-J3Hr'


@cli.sync_command()
@click.option('--data-path', default='juniorguru/data/followers.jsonl', type=click.Path(path_type=Path))
@click.option('--flush-data/--no-flush-data', default=False)
def main(data_path, flush_data):
    if flush_data and data_path.exists():
        logger.debug(f'Flushing {data_path}')
        data_path.unlink()

    today = date.today()
    if record := find_record(data_path, today):
        logger.info(f"Date {today!r} already recorded as {record!r}")
        return

    scrapers = {'youtube': scrape_youtube,
                'linkedin': scrape_linkedin,
                'linkedin_personal': scrape_linkedin_personal}
    logger.info(f"Scraping: {', '.join(scrapers.keys())}")

    data = {name: scrape() for name, scrape in scrapers.items()}
    data['date'] = today.isoformat()
    logger.info(f"Results: {data!r}")

    with open(data_path, mode='a') as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True))
        f.write('\n')


def find_record(path, date):
    try:
        logger.debug(f"Looking for {date!r} in {path}")
        with open(path, mode='r') as f:
            for line in f:
                if date.isoformat() in line:
                    return json.loads(line)
        return None
    except FileNotFoundError:
        return None


def scrape_youtube():
    logger.info('Scraping YouTube')
    session = requests.Session()
    response = session.get(YOUTUBE_URL)
    response.raise_for_status()
    html_tree = html.fromstring(response.content)
    try:
        consent_form = [form for form in html_tree.forms
                        if form.action == YOUTUBE_CONSENT_FORM_URL][0]
        response = session.request(consent_form.method.lower(),
                                   consent_form.action,
                                   params=consent_form.form_values())
        response.raise_for_status()
    except IndexError:
        logger.warning('There is no YouTube consent form')
    match = re.search(r'"(\d+) (odběratelů|subscribers)"', response.text)
    try:
        return int(match.group(1))
    except AttributeError:
        logger.error(f"Scraping failed!\n\n{response.text}")
        return None


def scrape_linkedin():
    logger.info('Scraping LinkedIn')
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(LINKEDIN_URL, wait_until='networkidle')
        if '/authwall' in page.url:
            logger.error(f'Loaded {page.url}')
            return None
        response_text = str(page.content())
        browser.close()
    match = re.search(r'Junior Guru \| (\d+) followers on LinkedIn.', response_text)
    try:
        return int(match.group(1))
    except (AttributeError, ValueError):
        logger.error(f"Scraping failed!\n\n{response_text}")
        return None


def scrape_linkedin_personal():
    logger.info('Scraping personal LinkedIn')
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(LINKEDIN_PERSONAL_URL, wait_until='networkidle')
        if '/authwall' in page.url:
            logger.error(f'Loaded {page.url}')
            return None
        response_text = str(page.content())
        browser.close()
    match = re.search(r'([\d,]+)\s*(followers|sledujících)', response_text)
    try:
        return int(match.group(1).replace(',', ''))
    except (AttributeError, ValueError):
        logger.error(f"Scraping failed!\n\n{response_text}")
        return None
