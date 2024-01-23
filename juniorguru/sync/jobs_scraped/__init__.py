from collections import Counter
import importlib
import itertools
from pprint import pformat

from peewee import IntegrityError

from juniorguru.lib import apify, loggers
from juniorguru.cli.sync import main as cli
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
    "juniorguru.sync.jobs_scraped.pipelines.features_parser",
    "juniorguru.sync.jobs_scraped.pipelines.gender_remover",
    "juniorguru.sync.jobs_scraped.pipelines.emoji_remover",
    "juniorguru.sync.jobs_scraped.pipelines.company_url_cleaner",
    "juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner",
    "juniorguru.sync.jobs_scraped.pipelines.juniority_re_score",
]


logger = loggers.from_path(__file__)


class DropItem(Exception):
    pass


@cli.sync_command()
@db.connection_context()
def main():
    logger.debug(f"Actors: {pformat(ACTORS)}")
    items = itertools.chain.from_iterable(apify.iter_data(actor) for actor in ACTORS)

    logger.debug(f"Pipelines: {pformat(PIPELINES)}")
    pipelines = [
        (
            pipeline_name.split(".")[-1],
            importlib.import_module(pipeline_name).process,
        )
        for pipeline_name in PIPELINES
    ]

    stats = Counter()
    for item in logger.progress(items):
        logger.debug(f"Item {item['url']}")
        try:
            for pipeline_name, pipeline in pipelines:
                try:
                    item = pipeline(item)
                except DropItem as e:
                    logger[pipeline_name].debug(f"Dropping: {e}\n{pformat(item)}")
                    raise
                except Exception:
                    logger.error(f"Pipeline {pipeline_name!r} failed:\n{pformat(item)}")
                    raise
        except DropItem:
            stats["drops"] += 1
        else:
            stats["items"] += 1

        job = ScrapedJob.from_item(item)
        try:
            logger.debug(f"Saving {item['url']} as {job!r}")
            job.save()
        except IntegrityError:
            logger.debug(f"Merging {item['url']} to {job!r}")
            job = ScrapedJob.get_by_item(item)
            job.merge_item(item)
            job.save()
    logger.info(
        f"Stats: {stats['items']} items, "
        f"{stats['drops']} drops, "
        f"{stats['items'] + stats['drops']} total"
    )
