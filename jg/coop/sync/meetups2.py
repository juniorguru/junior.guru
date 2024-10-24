from pathlib import Path

import click
import yaml
from openai import BaseModel
from pydantic import HttpUrl, field_validator

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.mapycz import REGIONS
from jg.coop.lib.yaml import YAMLConfig


YAML_PATH = Path("jg/coop/data/meetups.yml")


logger = loggers.from_path(__file__)


class GroupConfig(BaseModel):
    group_url: HttpUrl
    regions: list[str]

    @field_validator("regions")
    @classmethod
    def validate_regions(cls, value: list[str]) -> list[str]:
        for region in value:
            if region not in REGIONS:
                raise ValueError(
                    f"Invalid region {region!r}, expected one of {REGIONS})"
                )
        return value


class MeetupsConfig(YAMLConfig):
    groups: list[GroupConfig]


@cli.sync_command(dependencies=["club-content"])
@click.option(
    "--config",
    "config_path",
    default="jg/coop/data/meetups.yml",
    type=click.Path(exists=True, path_type=Path),
)
def main(config_path: Path):
    logger.info(f"Reading {config_path.name}")
    yaml_data = yaml.safe_load(config_path.read_text())
    config = MeetupsConfig(**yaml_data)
    print(config)
