from collections.abc import Iterable

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.job import JobTag, ListedJob, Tag


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-locations", "jobs-tech-tags"])
@db.connection_context()
def main():
    JobTag.drop_table()
    JobTag.create_table()
    for job in ListedJob.listing():
        rows = get_tag_rows(job.id, job.tags)
        logger.debug(f"{job!r}: {len(rows)} tags")
        if rows:
            JobTag.insert_many(rows).execute()
    logger.info(f"Saved {JobTag.select().count()} tags")


def get_tag_rows(job_id: int, tags: Iterable[Tag]) -> list[dict]:
    """
    Turns tags of a job into unique database rows, keeping their order
    """
    return [
        {"job": job_id, "type": str(tag.type), "slug": tag.slug}
        for tag in dict.fromkeys(tags)
    ]
