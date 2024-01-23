import os
from typing import Generator
import copy

from apify_client import ApifyClient
from apify_shared.consts import ActorJobStatus
from diskcache import Cache

from juniorguru.lib import loggers


APIFY_API_KEY = os.environ.get("APIFY_API_KEY")


logger = loggers.from_path(__file__)


def iter_data(
    actor_name: str,
    token: str | None = None,
    cache: Cache | None = None,
) -> Generator[dict, None, None]:
    cache_key = f"apify_{actor_name}"
    items = cache.get(cache_key) if cache else None
    if items:
        logger.debug(f"Found cached {actor_name} items: {len(items)}")
        yield from items
    else:
        client = ApifyClient(token=token or APIFY_API_KEY)

        logger.debug(f"Getting last successful run of {actor_name}")
        actor = client.actor(actor_name)
        last_run = actor.last_run(status=ActorJobStatus.SUCCEEDED)
        run_info = last_run.get()
        if run_info is None:
            raise RuntimeError(f"No successful runs of {actor_name!r} found")
        run_url = f"https://console.apify.com/actors/{run_info['actId']}/runs/{run_info['id']}"

        logger.debug(
            f"Last successful run of {actor_name}: {run_url}, "
            f"finished {run_info['finishedAt']}, "
            f"took {run_info['stats']['runTimeSecs']}s"
        )
        dataset = last_run.dataset()

        logger.debug("Iterating over dataset")
        if cache:
            items = []
            for item in dataset.iterate_items():
                items.append(item)
                yield copy.deepcopy(item)
            logger.debug(f"Caching {len(items)} {actor_name} items")
            cache.set(cache_key, items)
        else:
            yield from dataset.iterate_items()
