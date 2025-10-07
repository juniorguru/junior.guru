from pathlib import Path

import click
import httpx

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cache import get_cache
from jg.coop.lib.cli import async_command
from jg.coop.lib.memberful import MemberfulAPI
from jg.coop.models.base import db


MEMBERS_GQL_PATH = Path(__file__).parent / "members.gql"


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option("--cache-key", default="newsletter:subscribers")
@click.option("--cache-hrs", default=60, type=int)
@click.option("--ecomail-api-key", default=default_from_env("ECOMAIL_API_KEY"))
@click.option("--ecomail-list", "ecomail_list_id", default=1, type=int)
@db.connection_context()
@async_command
async def main(
    cache_key: str, cache_hrs: int, ecomail_api_key: str, ecomail_list_id: int
):
    cache = get_cache()
    if subscribers := cache.get(cache_key):
        logger.info(f"Using cached {len(subscribers)} subscribers")
    else:
        subscribers = {}

        logger.info("Fetching subscribers from Memberful")
        memberful = MemberfulAPI()
        for member in memberful.get_nodes(MEMBERS_GQL_PATH.read_text()):
            subscribers.setdefault(member["email"], set())
            subscribers[member["email"]].add("memberful")
        logger.info(f"Fetched {len(subscribers)} subscribers from Memberful")

        logger.info("Fetching subscribers from Ecomail")
        # According to https://ecomailczv2.docs.apiary.io/
        # Status = 1: subscribed, 2: unsubscribed, 3: soft bounce, 4: hard bounce, 5: spam complaint, 6: unconfirmed
        ecomail_page_url = (
            f"https://api2.ecomailapp.cz/lists/{ecomail_list_id}/subscribers"
        )
        ecomail_headers = {
            "key": ecomail_api_key,
            "User-Agent": "JuniorGuruBot (+https://junior.guru)",
        }
        ecomail_count = 0
        async with httpx.AsyncClient(headers=ecomail_headers) as client:
            for page in range(1, 100):  # safety break at 100 pages
                logger.debug(f"Getting subscribers from {ecomail_page_url}")
                response = await client.get(
                    ecomail_page_url,
                    params={"status": 1, "per_page": 100, "page": page},
                )
                logger.debug(f"Parsing response: {response.url}")
                response.raise_for_status()
                response_json = response.json()
                for subscriber in response_json["data"]:
                    source = (
                        "mailchimp"
                        if subscriber["source"] == "mailchimp"
                        else "ecomail"
                    )
                    subscribers.setdefault(subscriber["email"], set())
                    subscribers[subscriber["email"]].add(source)
                    ecomail_count += 1
                if response_json["next_page_url"]:
                    logger.debug(
                        f"Fetched {ecomail_count} subscribers so far, "
                        f"{response_json['per_page']} per page, "
                        f"{response_json['total']} total"
                    )
                else:
                    logger.info(f"Fetched {ecomail_count} subscribers from Ecomail")
                    break
        logger.debug("Caching subscribers")
        cache.set(cache_key, subscribers, expire=3600 * cache_hrs, tag="subscribers")

    return  # TODO

    logger.info(f"Adding {len(subscribers)} subscribers to Buttondown")
    for email, sources in logger.progress(subscribers.items()):
        async with ButtondownAPI() as buttondown:
            logger.debug(f"Adding subscriber {email} from {sources}")
            await buttondown.add_subscriber(email=email, tags=sources)
