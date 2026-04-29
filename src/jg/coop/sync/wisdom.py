from datetime import date
from pathlib import Path
from textwrap import shorten

import click
import yaml

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.wisdom import Wisdom


logger = loggers.from_path(__file__)


class WisdomConfig(YAMLConfig):
    date: date
    text: str
    name: str


@cli.sync_command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/wisdom.yml"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    Wisdom.drop_table()
    Wisdom.create_table()
    yaml_data = yaml.safe_load(path.read_text())
    for config in [WisdomConfig(**yaml_record) for yaml_record in yaml_data]:
        record = config.model_dump()
        logger.info(
            f"{record['name']}: {shorten(record['text'], width=20, placeholder='…')}"
        )
        Wisdom.create(**record)
