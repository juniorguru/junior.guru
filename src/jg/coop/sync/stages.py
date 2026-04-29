from pathlib import Path

import click
import yaml

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.stage import Stage


logger = loggers.from_path(__file__)


class StageConfig(YAMLConfig):
    slug: str
    icon: str
    title: str
    description: str


@cli.sync_command()
@click.option(
    "--path",
    default=Path("src/jg/coop/data/stages.yml"),
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@db.connection_context()
def main(path: Path):
    Stage.drop_table()
    Stage.create_table()
    yaml_data = yaml.safe_load(path.read_text())
    configs = [StageConfig(**yaml_record) for yaml_record in yaml_data]
    for position, config in enumerate(configs, start=1):
        logger.info(f"#{position} {config.title}")
        Stage.create(position=position, **config.model_dump())
