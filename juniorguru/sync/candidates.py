from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.candidate import Candidate


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['club-content', 'roles'])
@db.connection_context()
def main():
    Candidate.drop_table()
    Candidate.create_table()
