import asyncio
import importlib
import itertools
from pprint import pformat
from typing import Awaitable, Callable

from peewee import IntegrityError

from juniorguru.cli.sync import main as cli
from juniorguru.lib import apify, loggers
from juniorguru.lib.cli import async_command
from juniorguru.models.base import db
from juniorguru.models.job import ScrapedJob


ACTORS = [
    "honzajavorek/jobs-jobscz",
    "honzajavorek/jobs-linkedin",
    "honzajavorek/jobs-startupjobs",
    "honzajavorek/jobs-weworkremotely",
]

PIPELINES = [
    "juniorguru.sync.jobs_scraped.pipelines.blocklist",
    "juniorguru.sync.jobs_scraped.pipelines.boards_ids",
    "juniorguru.sync.jobs_scraped.pipelines.description_parser",
    "juniorguru.sync.jobs_scraped.pipelines.llm_opinion",
    "juniorguru.sync.jobs_scraped.pipelines.features_parser",
    "juniorguru.sync.jobs_scraped.pipelines.gender_remover",
    "juniorguru.sync.jobs_scraped.pipelines.emoji_remover",
    "juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner",
    "juniorguru.sync.jobs_scraped.pipelines.juniority_re_score",
]


logger = loggers.from_path(__file__)


class DropItem(Exception):
    pass


# Python 3.12 should start supporting generators for asyncio.as_completed,
# so remove this class then
class DisguisedGenerator:
    def __init__(self, generator):
        self._generator = generator

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)

    def __len__(self):
        raise NotImplementedError("DisguisedGenerator doesn't support len()")

    def __getitem__(self, index):
        raise NotImplementedError("DisguisedGenerator doesn't support indexing")


@cli.sync_command()
@async_command
async def main():
    logger.info(f"Actors:\n{pformat(ACTORS)}")
    items = itertools.chain.from_iterable(apify.fetch_data(actor) for actor in ACTORS)

    logger.info(f"Pipelines:\n{pformat(PIPELINES)}")
    pipelines = [
        (
            pipeline_name.split(".")[-1],
            importlib.import_module(pipeline_name).process,
        )
        for pipeline_name in PIPELINES
    ]

    logger.info("Setting up db table")
    with db.connection_context():
        ScrapedJob.drop_table()
        ScrapedJob.create_table()

    logger.info("Processing items")
    # tasks = [
    #     asyncio.create_task(process_item(pipelines, item))
    #     for item in items
    # ]
    # count = sum(await asyncio.gather(*tasks))

    count = 0
    drops = 0
    for processing in logger.progress(
        asyncio.as_completed(
            DisguisedGenerator(process_item(pipelines, item) for item in items)
        )
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
        return 0

    logger.debug(f"Saving {item['url']}")
    await asyncio.get_running_loop().run_in_executor(None, save_item, item)
    return 1


@db.connection_context()
def save_item(item: dict) -> None:
    job = ScrapedJob.from_item(item)
    try:
        job.save()
        logger.debug(f"Created {item['url']} as {job!r}")
    except IntegrityError:
        job = ScrapedJob.get_by_item(item)
        job.merge_item(item)
        job.save()
        logger.debug(f"Merged {item['url']} to {job!r}")
