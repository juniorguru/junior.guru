from pathlib import Path

from strictyaml import Map, Seq, Str, Url, load

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.yaml import Date
from jg.coop.models.base import db
from jg.coop.models.story import Story


YAML_PATH = Path("src/jg/coop/data/stories.yml")

YAML_SCHEMA = Seq(
    Map(
        {
            "url": Url(),
            "date": Date(),
            "title": Str(),
            "name": Str(),
            "image_path": Str(),
            "tags": Seq(Str()),
        }
    )
)


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    Story.drop_table()
    Story.create_table()
    for yaml_record in load(YAML_PATH.read_text(), YAML_SCHEMA):
        record = yaml_record.data
        logger.info(record["title"])
        Story.create(**record)
