import os
from datetime import timedelta
from functools import lru_cache
from typing import Generator

from apify_client import ApifyClient
from apify_shared.consts import ActorJobStatus

from jg.coop.lib import loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.mutations import mutates


APIFY_API_KEY = os.getenv("APIFY_API_KEY")


logger = loggers.from_path(__file__)


@lru_cache
def create_client(token: str | None = None) -> ApifyClient:
    return ApifyClient(token=token or APIFY_API_KEY)


@mutates("apify", raises=True)
def run(
    actor_name: str, run_input: dict | None = None, token: str | None = None
) -> list[dict]:
    client = create_client(token=token)
    actor = client.actor(actor_name)

    logger.debug(f"Starting {actor_name}")
    run_info = actor.start(run_input=run_input)
    run = client.run(run_info["id"])

    logger.debug(f"Waiting for {actor_name}")
    run_info = run.wait_for_finish()

    logger.debug(f"Finished! {run_info!r}")
    if run_info["status"] != ActorJobStatus.SUCCEEDED:
        raise RuntimeError(f"Run of {actor_name} failed: {run_info!r}")

    return list(run.dataset().iterate_items())


@cache(expire=timedelta(days=1), tag="apify")
def fetch_data(
    actor_name: str,
    token: str | None = None,
    raise_if_missing: bool = True,
) -> list[dict]:
    client = create_client(token=token)

    logger.debug(f"Getting last successful run of {actor_name}")
    actor = client.actor(actor_name)
    last_run = actor.last_run(status=ActorJobStatus.SUCCEEDED)
    run_info = last_run.get()
    if run_info is None:
        if raise_if_missing:
            raise RuntimeError(f"No successful runs of {actor_name!r} found")
        logger.error(f"No successful runs of {actor_name!r} found")
        return []

    run_url = (
        f"https://console.apify.com/actors/{run_info['actId']}/runs/{run_info['id']}"
    )
    logger.debug(
        f"Last successful run of {actor_name}: {run_url}, "
        f"finished {run_info['finishedAt']}, "
        f"took {run_info['stats']['runTimeSecs']}s"
    )
    dataset = last_run.dataset()
    return list(dataset.iterate_items())


@cache(expire=timedelta(days=1), tag="apify")
def fetch_scheduled_actors(token: str | None = None) -> list[str]:
    client = create_client(token=token)
    schedules = [
        schedule
        for schedule in client.schedules().list().items
        if schedule["isEnabled"]
    ]
    actor_ids = set()
    for schedule in schedules:
        schedule_actor_ids = [
            action["actorId"]
            for action in schedule["actions"]
            if action["type"] == "RUN_ACTOR"
        ]
        actor_ids.update(schedule_actor_ids)
    return [
        f"{actor_info['username']}/{actor_info['name']}"
        for actor_info in (client.actor(actor_id).get() for actor_id in actor_ids)
    ]
