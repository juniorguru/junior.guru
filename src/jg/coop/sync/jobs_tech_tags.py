from jg.beak.core import beak

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.job import ListedJob


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["jobs-listing"])
@db.connection_context()
def main():
    for job in ListedJob.listing():
        job.tech_tags = list(map(str, beak(job.description_text)))
        job.save()
