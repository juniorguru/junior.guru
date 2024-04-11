from project.cli.sync import main as cli
from project.lib import loggers
from project.models.base import db
from project.models.candidate import Candidate


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["club-content", "roles"])
@db.connection_context()
def main():
    Candidate.drop_table()
    Candidate.create_table()
