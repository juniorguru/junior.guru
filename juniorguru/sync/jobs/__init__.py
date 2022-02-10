from pathlib import Path

from juniorguru.lib.timer import measure
from juniorguru.models import db, Job
from juniorguru.jobs.settings import FEEDS_DIR
from juniorguru.sync.jobs.processing import filter_relevant_paths, process_paths, postprocess_jobs


TRAILING_DAYS = 365
PREPROCESS_PIPELINES = [
    'juniorguru.sync.jobs.pipelines.identify',
]
POSTPROCESS_PIPELINES = [
    'juniorguru.sync.jobs.pipelines.locations',
    'juniorguru.sync.jobs.pipelines.description_parser',
    'juniorguru.sync.jobs.pipelines.features_parser',
    'juniorguru.sync.jobs.pipelines.gender_cleaner',
    'juniorguru.sync.jobs.pipelines.emoji_cleaner',
    'juniorguru.sync.jobs.pipelines.employment_types_cleaner',
]


@measure('jobs')
def main():
    with db.connection_context():
        Job.drop_table()
        Job.create_table()

    paths = Path(FEEDS_DIR).glob('**/*.jsonl')
    paths = filter_relevant_paths(paths, TRAILING_DAYS)
    process_paths(paths, PREPROCESS_PIPELINES)
    postprocess_jobs(POSTPROCESS_PIPELINES)
