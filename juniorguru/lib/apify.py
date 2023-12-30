import os
from typing import Generator
from apify_client import ApifyClient
from apify_shared.consts import ActorJobStatus

from juniorguru.lib import loggers


APIFY_API_KEY = os.environ.get("APIFY_API_KEY")


logger = loggers.from_path(__file__)


def iter_data(actor_name: str, token=None) -> Generator[dict, None, None]:
    client = ApifyClient(token=token or APIFY_API_KEY)
    logger.debug(f"Getting last successful run of {actor_name}")
    actor = client.actor(actor_name)
    last_run = actor.last_run(status=ActorJobStatus.SUCCEEDED)
    run_info = last_run.get()
    run_url = f"https://console.apify.com/actors/{run_info['actId']}/runs/{run_info['id']}"
    logger.debug(f"Last successful run of {actor_name}: {run_url}, finished {run_info['finishedAt']}, took {run_info['stats']['runTimeSecs']}s")
    dataset = last_run.dataset()
    logger.debug("Iterating over dataset")
    yield from dataset.iterate_items()
