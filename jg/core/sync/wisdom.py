from pathlib import Path
from textwrap import shorten

from strictyaml import Map, Seq, Str, load

from jg.core.cli.sync import main as cli
from jg.core.lib import loggers
from jg.core.lib.yaml import Date
from jg.core.models.base import db
from jg.core.models.wisdom import Wisdom


YAML_PATH = Path("jg/core/data/wisdom.yml")

YAML_SCHEMA = Seq(
    Map(
        {
            "date": Date(),
            "text": Str(),
            "name": Str(),
        }
    )
)


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    Wisdom.drop_table()
    Wisdom.create_table()
    for yaml_record in load(YAML_PATH.read_text(), YAML_SCHEMA):
        record = yaml_record.data
        logger.info(
            f"{record['name']}: {shorten(record['text'], width=20, placeholder='…')}"
        )
        Wisdom.create(**record)
