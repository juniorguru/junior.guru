from datetime import date
from pathlib import Path
from typing import Annotated

import click
import yaml
from pydantic import HttpUrl, PlainSerializer

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.external_story import ExternalStory


logger = loggers.from_path(__file__)


class ExternalStoryConfig(YAMLConfig):
    url: Annotated[HttpUrl, PlainSerializer(str)]
    date: date
    title: str
    name: str
    image_path: str
    tags: list[str]


@cli.sync_command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/external-stories.yml"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    ExternalStory.drop_table()
    ExternalStory.create_table()
    yaml_data = yaml.safe_load(path.read_text())
    for config in [ExternalStoryConfig(**yaml_record) for yaml_record in yaml_data]:
        record = config.model_dump()
        logger.info(record["title"])
        ExternalStory.create(**record)
