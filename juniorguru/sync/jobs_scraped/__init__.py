import os
from pathlib import Path

from peewee import OperationalError

from juniorguru.lib import loggers
from juniorguru.cli.sync import main as cli
from juniorguru.models.base import db
from juniorguru.models.job import ScrapedJob
from juniorguru.sync.jobs_scraped.processing import (filter_relevant_paths,
                                                     postprocess_jobs, process_paths)
from juniorguru.sync.scrape_jobs.settings import FEEDS_DIR


JOBS_SCRAPED_REUSE_DB_ENABLED = bool(int(os.getenv('JOBS_SCRAPED_REUSE_DB_ENABLED', 0)))

PREPROCESS_PIPELINES = [
    'juniorguru.sync.jobs_scraped.pipelines.boards_ids',
]

POSTPROCESS_PIPELINES = [
    'juniorguru.sync.jobs_scraped.pipelines.description_parser',
    'juniorguru.sync.jobs_scraped.pipelines.features_parser',
    'juniorguru.sync.jobs_scraped.pipelines.gender_cleaner',
    'juniorguru.sync.jobs_scraped.pipelines.emoji_cleaner',
    'juniorguru.sync.jobs_scraped.pipelines.company_url_cleaner',
    'juniorguru.sync.jobs_scraped.pipelines.employment_types_cleaner',
    'juniorguru.sync.jobs_scraped.pipelines.juniority_re_score',
]


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['scrape-jobs'])
def main():
    paths = list(Path(FEEDS_DIR).glob('**/*.jsonl.gz'))
    logger.info(f'Found {len(paths)} .json.gz paths')

    latest_seen_on = None
    with db.connection_context():
        if JOBS_SCRAPED_REUSE_DB_ENABLED:
            logger.warning('Reusing of existing jobs database is enabled!')
            try:
                latest_seen_on = ScrapedJob.latest_seen_on()
                logger.info(f'Last jobs seen on: {latest_seen_on}')
            except OperationalError:
                logger.warning('Jobs database not operational!')

        if latest_seen_on:
            paths = filter_relevant_paths(paths, latest_seen_on)
            logger.info(f'Keeping {len(paths)} relevant .json.gz paths')
        else:
            logger.info('Not reusing jobs database')
            ScrapedJob.drop_table()
            ScrapedJob.create_table()

    process_paths(paths, PREPROCESS_PIPELINES)
    postprocess_jobs(POSTPROCESS_PIPELINES)
