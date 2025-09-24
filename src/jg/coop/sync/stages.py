from pathlib import Path

from strictyaml import Map, Seq, Str, load

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.stage import Stage


YAML_PATH = Path("jg/coop/data/stages.yml")

YAML_SCHEMA = Seq(
    Map(
        {
            "slug": Str(),
            "icon": Str(),
            "title": Str(),
            "description": Str(),
        }
    )
)


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    Stage.drop_table()
    Stage.create_table()
    records = (
        yaml_record.data for yaml_record in load(YAML_PATH.read_text(), YAML_SCHEMA)
    )
    for position, record in enumerate(records, start=1):
        logger.info(f"#{position} {record['title']}")
        Stage.create(position=position, **record)
