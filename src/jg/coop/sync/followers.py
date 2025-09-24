import re
from datetime import date
from functools import partial
from pathlib import Path

import click
import requests
from githubkit import GitHub
from lxml import html

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import apify, loggers
from jg.coop.models.base import db
from jg.coop.models.followers import Followers


logger = loggers.from_path(__file__)


YOUTUBE_URL = "https://www.youtube.com/@juniordotguru"

YOUTUBE_CONSENT_FORM_URL = "https://consent.youtube.com/save"

YOUTUBE_LANGUAGE_FORM_URL = "https://consent.youtube.com/ml"

LINKEDIN_URL = "https://www.linkedin.com/company/juniorguru"

LINKEDIN_PERSONAL_SEARCH_URL = (
    "https://duckduckgo.com/?q=honza+javorek+site%3Alinkedin.com&ia=web"
)

GITHUB_USERNAME = "juniorguru"

GITHUB_PERSONAL_USERNAME = "honzajavorek"


@cli.sync_command()
@click.option(
    "--history-path",
    default="jg/coop/data/followers.jsonl",
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

    logger.info("Getting scraped followers")
    for item in apify.fetch_data("honzajavorek/followers"):
        Followers.add(month=item["date"][:7], name=item["name"], count=item["count"])

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
    # TODO move to Plucker
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


def scrape_github_personal(api_key: str) -> int:
    logger.info("Scraping personal GitHub")
    with GitHub(api_key) as github:
        response = github.rest.users.get_by_username(GITHUB_PERSONAL_USERNAME)
        user = response.parsed_data
        return user.followers


def scrape_github(api_key: str) -> int:
    logger.info("Scraping GitHub")
    with GitHub(api_key) as github:
        response = github.rest.orgs.get(GITHUB_USERNAME)
        org = response.parsed_data
        return org.followers
