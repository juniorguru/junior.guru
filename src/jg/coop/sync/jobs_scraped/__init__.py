import asyncio
import importlib
import itertools
from pprint import pformat
from typing import Awaitable, Callable

from peewee import IntegrityError

from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.lib.async_utils import make_async
from jg.coop.lib.cli import async_command
from jg.coop.models.base import db
from jg.coop.models.job import DroppedJob, ScrapedJob
from jg.coop.sync.jobs_scraped import linkedin


PIPELINES = [
    "jg.coop.sync.jobs_scraped.pipelines.time_filter",
    "jg.coop.sync.jobs_scraped.pipelines.blocklist_filter",
    "jg.coop.sync.jobs_scraped.pipelines.broken_encoding_filter",
    "jg.coop.sync.jobs_scraped.pipelines.description_parser",
    "jg.coop.sync.jobs_scraped.pipelines.language_parser",
    "jg.coop.sync.jobs_scraped.pipelines.language_filter",
    "jg.coop.sync.jobs_scraped.pipelines.llm_opinion",
    "jg.coop.sync.jobs_scraped.pipelines.relevance_filter",
    "jg.coop.sync.jobs_scraped.pipelines.boards_ids",
    "jg.coop.sync.jobs_scraped.pipelines.gender_remover",
    "jg.coop.sync.jobs_scraped.pipelines.emoji_remover",
    "jg.coop.sync.jobs_scraped.pipelines.url_fixer",
    "jg.coop.sync.jobs_scraped.pipelines.employment_types_cleaner",
]


logger = loggers.from_path(__file__)


class DropItem(Exception):
    pass


@cli.sync_command()
@async_command
async def main():
    scheduled_actor_names = apify.fetch_scheduled_actors()
    jobs_actor_names = [
        actor_name
        for actor_name in scheduled_actor_names
        if actor_name.startswith("honzajavorek/jobs-")
    ]
    logger.info(f"Actors:\n{pformat(jobs_actor_names)}")
    items = itertools.chain.from_iterable(
        apify.fetch_data(actor_name, raise_if_missing=False)
        for actor_name in jobs_actor_names
    )

    if linkedin.ACTOR_NAME in scheduled_actor_names:
        logger.info(f"LinkedIn Actor: {linkedin.ACTOR_NAME}")
        linkedin_items = apify.fetch_data(linkedin.ACTOR_NAME, raise_if_missing=False)
        items = itertools.chain(items, map(linkedin.transform_item, linkedin_items))

    logger.info(f"Pipelines:\n{pformat(PIPELINES)}")
    pipelines = [
        (
            pipeline_name.split(".")[-1],
            importlib.import_module(pipeline_name).process,
        )
        for pipeline_name in PIPELINES
    ]

    logger.info("Setting up db tables")
    with db.connection_context():
        db.drop_tables([DroppedJob, ScrapedJob])
        db.create_tables([DroppedJob, ScrapedJob])

    logger.info("Processing items")
    count = 0
    drops = 0
    for processing in logger.progress(
        asyncio.as_completed(process_item(pipelines, item) for item in items)
    ):
        count += 1
        drops += 1 - (await processing)
    logger.info(f"Stats: {count} items, {drops} drops")


async def process_item(
    pipelines: list[tuple[str, Callable[..., Awaitable[dict]]]],
    item: dict,
) -> int:
    logger.debug(f"Item {item['url']}")
    try:
        for pipeline_name, pipeline in pipelines:
            try:
                item = await pipeline(item)
            except DropItem as e:
                logger[pipeline_name].debug(f"Dropping: {e}\n{pformat(item)}")
                raise
            except Exception:
                logger.error(f"Pipeline {pipeline_name!r} failed:\n{pformat(item)}")
                raise
    except DropItem:
        logger.debug(f"Saving dropped job {item['url']}")
        await save_dropped_job(item)
        return 0

    logger.debug(f"Saving scraped job {item['url']}")
    await save_scraped_job(item)
    return 1


@make_async
@db.connection_context()
def save_scraped_job(item: dict) -> None:
    job = ScrapedJob.from_item(item)
    try:
        job.save()
        logger.debug(f"Created {item['url']} as {job!r}")
    except IntegrityError:
        job = ScrapedJob.get_by_item(item)
        job.merge_item(item)
        job.save()
        logger.debug(f"Merged {item['url']} to {job!r}")


@make_async
@db.connection_context()
def save_dropped_job(item: dict) -> None:
    job = DroppedJob.from_item(item)
    job.save()
    logger.debug(f"Created {item['url']} as {job!r}")
