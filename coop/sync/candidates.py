from coop.cli.sync import main as cli
from coop.lib import loggers
from coop.models.base import db
from coop.models.candidate import Candidate


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "roles"])
@db.connection_context()
def main():
    Candidate.drop_table()
    Candidate.create_table()
