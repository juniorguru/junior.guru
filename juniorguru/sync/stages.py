from pathlib import Path
from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.stage import Stage
from strictyaml import Map, Seq, Str, load


YAML_PATH = Path("juniorguru/data/stages.yml")

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
        logger.info(f'#{position} {record["title"]}')
        Stage.create(position=position, **record)
