import re
from pathlib import Path
from datetime import date

import json
import requests
from lxml import html
from playwright.sync_api import sync_playwright

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers


logger = loggers.from_path(__file__)


DATA_FILE = Path('juniorguru') / 'data' / 'followers.jsonl'

YOUTUBE_URL = 'https://www.youtube.com/@juniordotguru'

YOUTUBE_CONSENT_FORM_URL = 'https://consent.youtube.com/save'

YOUTUBE_LANGUAGE_FORM_URL = 'https://consent.youtube.com/ml'

LINKEDIN_URL = 'https://www.linkedin.com/company/juniorguru'

LINKEDIN_PERSONAL_URL = 'https://www.linkedin.com/in/honzajavorek/'


@cli.sync_command()
def main():
    today_iso = date.today().isoformat()

    with open(DATA_FILE, mode='r') as f:
        for line in f:
            if today_iso in line:
                logger.info(f"Date {today_iso} already recorded: {line.strip()}")
                return

    scrapers = {'youtube': scrape_youtube,
                'linkedin': scrape_linkedin,
                'linkedin_personal': scrape_linkedin_personal}
    logger.info(f"Scraping: {', '.join(scrapers.keys())}")

    data = {name: scrape() for name, scrape in scrapers.items()}
    data['date'] = today_iso
    logger.info(f"Results: {data!r}")

    with open(DATA_FILE, mode='a') as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True))
        f.write('\n')


def scrape_youtube():
    logger.info('Scraping YouTube')
    session = requests.Session()

    # get the consent page and set language to English
    response = session.get(YOUTUBE_URL)
    response.raise_for_status()
    html_tree = html.fromstring(response.content)
    language_form = [form for form in html_tree.forms
                    if form.action == YOUTUBE_LANGUAGE_FORM_URL][0]
    params = dict(language_form.form_values()) | dict(hl='cs', oldhl='cs', gl='CZ')
    response = session.get(YOUTUBE_LANGUAGE_FORM_URL, params=params)
    response.raise_for_status()

    # get the consent form
    consent_form = [form for form in html_tree.forms
                    if form.action == YOUTUBE_CONSENT_FORM_URL][0]
    response = session.request(consent_form.method.lower(), consent_form.action,
                               params=consent_form.form_values())
    response.raise_for_status()
    match = re.search(r'"(\d+) odběratelů"', response.text)
    return int(match.group(1))


def scrape_linkedin():
    logger.info('Scraping LinkedIn')
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(LINKEDIN_URL, wait_until='networkidle')
        response_text = str(page.content())
        browser.close()
    match = re.search(r'Junior Guru \| (\d+) followers on LinkedIn.', response_text)
    return int(match.group(1))


def scrape_linkedin_personal():
    logger.info('Scraping personal LinkedIn')
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(LINKEDIN_PERSONAL_URL, wait_until='networkidle')
        response_text = str(page.content())
        browser.close()
    match = re.search(r'"userInteractionCount":\s*(\d+)', response_text)
    return int(match.group(1))
