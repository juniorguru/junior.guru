from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.candidate import Candidate


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "roles"])
@db.connection_context()
def main():
    Candidate.drop_table()
    Candidate.create_table()
