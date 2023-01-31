from pathlib import Path

from strictyaml import Map, Seq, Str, Url, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.lib.yaml import Date
from juniorguru.models.base import db
from juniorguru.models.story import Story


YAML_PATH = Path('juniorguru/data/stories.yml')

YAML_SCHEMA = Seq(
    Map({
        'url': Url(),
        'date': Date(),
        'title': Str(),
        'image_path': Str(),
        'tags': Seq(Str()),
    })
)


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    Story.drop_table()
    Story.create_table()
    for yaml_record in load(YAML_PATH.read_text(), YAML_SCHEMA):
        record = yaml_record.data
        logger.info(record['title'])
        Story.create(**record)
