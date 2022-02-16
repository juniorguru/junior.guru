import os
from pathlib import Path

from peewee import OperationalError

from juniorguru.lib import loggers
from juniorguru.lib.timer import measure
from juniorguru.models import db, DownloadedJob
from juniorguru.jobs.settings import FEEDS_DIR
from juniorguru.sync.jobs.processing import filter_relevant_paths, process_paths, postprocess_jobs


REUSE_JOBS_DB_ENABLED = bool(int(os.getenv('REUSE_JOBS_DB_ENABLED', 0)))

PREPROCESS_PIPELINES = [
    'juniorguru.sync.jobs.pipelines.boards_ids',
]

POSTPROCESS_PIPELINES = [
    'juniorguru.sync.jobs.pipelines.locations',
    'juniorguru.sync.jobs.pipelines.description_parser',
    'juniorguru.sync.jobs.pipelines.features_parser',
    'juniorguru.sync.jobs.pipelines.gender_cleaner',
    'juniorguru.sync.jobs.pipelines.emoji_cleaner',
    'juniorguru.sync.jobs.pipelines.employment_types_cleaner',
]


logger = loggers.get('juniorguru.sync.jobs')


@measure('jobs')
def main():
    paths = list(Path(FEEDS_DIR).glob('**/*.jsonl.gz'))
    logger.info(f'Found {len(paths)} .json.gz paths')

    latest_seen_on = None
    with db.connection_context():
        if REUSE_JOBS_DB_ENABLED:
            logger.warning('Reusing of existing jobs database is enabled!')
            try:
                latest_seen_on = DownloadedJob.latest_seen_on()
                logger.info(f'Last jobs seen on: {latest_seen_on}')
            except OperationalError:
                logger.warning('Jobs database not operational!')

        if latest_seen_on:
            paths = filter_relevant_paths(paths, latest_seen_on)
            logger.info(f'Keeping {len(paths)} relevant .json.gz paths')
        else:
            logger.info('Not reusing jobs database')
            DownloadedJob.drop_table()
            DownloadedJob.create_table()

    process_paths(paths, PREPROCESS_PIPELINES)
    postprocess_jobs(POSTPROCESS_PIPELINES)
