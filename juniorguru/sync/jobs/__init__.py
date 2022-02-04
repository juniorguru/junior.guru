from pathlib import Path

from juniorguru.lib.timer import measure
from juniorguru.models import db, Job
from juniorguru.jobs.settings import FEEDS_DIR
from juniorguru.sync.jobs.processing import filter_relevant_paths, process_paths, postprocess_jobs


TRAILING_DAYS = 365
ITEM_PIPELINES = [
    # 'juniorguru.sync.jobs.item_pipelines.identify',
]
JOB_PIPELINES = [
    # 'juniorguru.sync.jobs.job_pipelines.locations',
    # 'juniorguru.sync.jobs.job_pipelines.description_parser',
    # 'juniorguru.sync.jobs.job_pipelines.features_parser',
    'juniorguru.sync.jobs.job_pipelines.emoji_cleaner',
    # 'juniorguru.sync.jobs.job_pipelines.gender_cleaner',
]


@measure('jobs')
def main():
    with db:
        Job.drop_table()
        Job.create_table()

    paths = Path(FEEDS_DIR).glob('**/*.jsonl')
    paths = filter_relevant_paths(paths, TRAILING_DAYS)
    process_paths(paths, ITEM_PIPELINES)

    postprocess_jobs(JOB_PIPELINES)
