import re
from datetime import date
from functools import partial
from pathlib import Path
from urllib.parse import urlencode, urlparse

import click
import requests
from github import Auth, Github
from lxml import html
from playwright.sync_api import TimeoutError, sync_playwright

from project.cli.sync import default_from_env, main as cli
from project.lib import loggers
from project.lib.text import extract_text
from project.models.base import db
from project.models.followers import Followers


logger = loggers.from_path(__file__)


YOUTUBE_URL = "https://www.youtube.com/@juniordotguru"

YOUTUBE_CONSENT_FORM_URL = "https://consent.youtube.com/save"

YOUTUBE_LANGUAGE_FORM_URL = "https://consent.youtube.com/ml"

LINKEDIN_URL = "https://www.linkedin.com/company/juniorguru"

LINKEDIN_PERSONAL_SEARCH_URL = "https://duckduckgo.com/?hps=1&q=honza+javorek&ia=web"

LINKEDIN_PERSONAL_URL = "https://cz.linkedin.com/in/honzajavorek"

GITHUB_USERNAME = "juniorguru"

GITHUB_PERSONAL_USERNAME = "honzajavorek"


@cli.sync_command()
@click.option(
    "--history-path",
    default="project/data/followers.jsonl",
    type=click.Path(path_type=Path),
)
@click.option("--ecomail-api-key", default=default_from_env("ECOMAIL_API_KEY"))
@click.option("--ecomail-list", "ecomail_list_id", default=1, type=int)
@click.option(
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
@db.connection_context()
def main(
    history_path: Path, ecomail_api_key: str, ecomail_list_id: int, github_api_key: str
):
    logger.info("Preparing database")
    Followers.drop_table()
    Followers.create_table()

    logger.info("Reading history from a file")
    history_path.touch(exist_ok=True)
    with history_path.open() as f:
        for line in f:
            Followers.deserialize(line)

    month = f"{date.today():%Y-%m}"
    logger.info(f"Current month: {month}")

    logger.info("Getting newsletter subscribers from Ecomail")
    try:
        response = requests.get(
            f"https://api2.ecomailapp.cz/lists/{ecomail_list_id}/subscribers",
            headers={
                "key": ecomail_api_key,
                "User-Agent": "JuniorGuruBot (+https://junior.guru)",
            },
        )
        response.raise_for_status()
        subscribers_count = response.json()["total"]
        Followers.add(month=month, name="newsletter", count=subscribers_count)
    except Exception:
        logger.exception("Failed to get newsletter subscribers")

    scrapers = {
        "youtube": scrape_youtube,
        "linkedin": scrape_linkedin,
        "linkedin_personal": scrape_linkedin_personal,
        "mastodon": scrape_mastodon,
        "github": partial(scrape_github, api_key=github_api_key),
        "github_personal": partial(scrape_github_personal, api_key=github_api_key),
    }
    for name, scrape in scrapers.items():
        logger.info(f"Scraping {name!r}")
        if count := scrape():
            logger.info(f"Saving result: {count}")
            Followers.add(month=month, name=name, count=count)
        else:
            logger.warning(f"Result: {count}")

    logger.info("Saving history to a file")
    with history_path.open("w") as f:
        for db_object in Followers.history():
            f.write(db_object.serialize())


def scrape_youtube():
    logger.info("Scraping YouTube")
    session = requests.Session()
    response = session.get(YOUTUBE_URL)
    response.raise_for_status()
    html_tree = html.fromstring(response.content)
    try:
        consent_form = [
            form for form in html_tree.forms if form.action == YOUTUBE_CONSENT_FORM_URL
        ][0]
        response = session.request(
            consent_form.method.lower(),
            consent_form.action,
            params=consent_form.form_values(),
        )
        response.raise_for_status()
    except IndexError:
        logger.warning("There is no YouTube consent form")
    match = re.search(r'"(\d+) (odběratelů|subscribers)"', response.text)
    try:
        return int(match.group(1))
    except AttributeError:
        logger.error(f"Scraping failed!\n\n{response.text}")
        return None


def scrape_linkedin():
    logger.info("Scraping LinkedIn")
    text = None

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        # try LinkedIn first
        try:
            page.goto(LINKEDIN_URL, wait_until="networkidle")
            if "/authwall" in page.url:
                logger.error(f"Loaded {page.url}")
            else:
                text = str(page.content())
        except TimeoutError:
            logger.error(f"Time out on {LINKEDIN_URL}")

        # if we've got authwall or timeout, try Google results
        if text is None:
            google_query = f"{LINKEDIN_URL} sledujících"
            google_url = (
                f"https://www.google.cz/search?{urlencode(dict(q=google_query))}"
            )
            page.goto(google_url, wait_until="networkidle")
            html_tree = html.fromstring(page.content())
            html_link = html_tree.cssselect(f'a[href^="{LINKEDIN_URL}"]')[0]
            html_item = html_link.xpath("./ancestor::*[@data-hveid][position() = 1]")[0]
            text = extract_text(html.tostring(html_item))

    match = re.search(
        r"Junior Guru \| (\d+) (followers on|sledujících uživatelů na) LinkedIn.", text
    )
    try:
        return int(match.group(1))
    except (AttributeError, ValueError):
        logger.error(f"Scraping failed!\n\n{text}")
        return None


def scrape_linkedin_personal():
    logger.info("Scraping personal LinkedIn")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(LINKEDIN_PERSONAL_SEARCH_URL, wait_until="networkidle")
        url_parts = urlparse(LINKEDIN_PERSONAL_URL)
        _, domain = url_parts.netloc.split(".", 1)
        page.click(f"a[href*='{domain}{url_parts.path}']")
        if "/authwall" in page.url:
            logger.error(f"Loaded {page.url}")
            return None
        response_text = str(page.content())
        browser.close()

    if match := re.search(
        r'"name":\s*"Follows"\s*,\s*"userInteractionCount":\s*(\d+)', response_text
    ):
        return int(match.group(1))

    logger.error(f"Scraping {page.url} failed!\n\n{response_text}")
    return None


def scrape_mastodon():
    logger.info("Scraping Mastodon")
    urls = [
        "https://mastodonczech.cz/@honzajavorek",
        "https://mastodon.social/@honzajavorek@mastodonczech.cz"
        "https://witter.cz/@honzajavorek@mastodonczech.cz",
    ]
    for url in urls:
        try:
            response = requests.get(
                url, headers={"User-Agent": "JuniorGuruBot (+https://junior.guru)"}
            )
            response.raise_for_status()
            html_tree = html.fromstring(response.content)
            description = html_tree.cssselect('meta[name="description"]')[0].get(
                "content"
            )
            match = re.search(
                r"(\d+)\s+(followers|sledujících)", description, re.IGNORECASE
            )
            return int(match.group(1))
        except Exception as e:
            details = f"\n\n{e.response.text}" if getattr(e, "response", None) else ""
            logger.exception(f"Scraping failed!{details}")
    return None


def scrape_github_personal(api_key: str):
    logger.info("Scraping personal GitHub")
    client = Github(auth=Auth.Token(api_key))
    return client.get_user(login=GITHUB_PERSONAL_USERNAME).followers


def scrape_github(api_key: str):
    logger.info("Scraping GitHub")
    client = Github(auth=Auth.Token(api_key))
    return client.get_organization(login=GITHUB_USERNAME).followers
