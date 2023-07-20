import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Generator
from urllib.parse import urlencode

import click
import requests
from lxml import html
from playwright.sync_api import sync_playwright

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.text import extract_text
from juniorguru.models.base import db
from juniorguru.models.followers import Followers


logger = loggers.from_path(__file__)


YOUTUBE_URL = 'https://www.youtube.com/@juniordotguru'

YOUTUBE_CONSENT_FORM_URL = 'https://consent.youtube.com/save'

YOUTUBE_LANGUAGE_FORM_URL = 'https://consent.youtube.com/ml'

LINKEDIN_URL = 'https://www.linkedin.com/company/juniorguru'

LINKEDIN_PERSONAL_URL = 'https://www.linkedin.com/posts/honzajavorek_courting-haskell-honza-javorek-activity-6625070791035756544-J3Hr'


@cli.sync_command()
@click.option('--data-path', default='juniorguru/data/followers.jsonl', type=click.Path(path_type=Path))
@db.connection_context()
def main(data_path):
    logger.info("Preparing database")
    Followers.drop_table()
    Followers.create_table()

    scrapers = {'youtube': scrape_youtube,
                'linkedin': scrape_linkedin,
                'linkedin_personal': scrape_linkedin_personal}
    logger.info(f"Scraping: {', '.join(scrapers.keys())}")

    data = {name: scrape() for name, scrape in scrapers.items()}
    data['_month'] = f'{date.today():%Y-%m}'
    line_new = json.dumps(data, ensure_ascii=False, sort_keys=True)
    logger.info(f"Results: {line_new}")

    already_in_file = False
    with open(data_path, mode='r') as f:
        for line in f:
            if line.strip() == line_new:
                already_in_file = True
            for record in parse_line(line):
                Followers.create(**record)

    if already_in_file:
        logger.info('Line already in the file')
    else:
        logger.info('Adding new line')
        with open(data_path, mode='a') as f:
            f.write(line_new)
            f.write('\n')
        for record in parse_line(line_new):
            Followers.create(**record)


def parse_line(line: str) -> Generator[dict[str, Any], None, None]:
    data = json.loads(line)
    month = data.pop('_month')
    for name, count in data.items():
        if count is not None:
            yield dict(month=month, name=name, count=count)


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
    text = None

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        # try LinkedIn first
        page.goto(LINKEDIN_URL, wait_until='networkidle')
        if '/authwall' in page.url:
            logger.error(f'Loaded {page.url}')
        else:
            text = str(page.content())

        # if we've got authwall, try Google results
        if text is None:
            google_query = f'{LINKEDIN_URL} sledujících'
            google_url = f'https://www.google.cz/search?{urlencode(dict(q=google_query))}'
            page.goto(google_url, wait_until='networkidle')
            html_tree = html.fromstring(page.content())
            html_link = html_tree.cssselect(f'a[href^="{LINKEDIN_URL}"]')[0]
            html_item = html_link.xpath('./ancestor::*[@data-hveid][position() = 1]')[0]
            text = extract_text(html.tostring(html_item))

    match = re.search(r'Junior Guru \| (\d+) (followers on|sledujících uživatelů na) LinkedIn.', text)
    try:
        return int(match.group(1))
    except (AttributeError, ValueError):
        logger.error(f"Scraping failed!\n\n{text}")
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


def parents(html_node):
    parent = html_node.getparent()
    while parent is not None:
        yield parent
        parent = parent.getparent()
