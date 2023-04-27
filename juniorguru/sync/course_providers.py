from pathlib import Path

from strictyaml import Map, Str, Url, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.course_provider import CourseProvider


YAML_DIR_PATH = Path('juniorguru/data/course_providers')

YAML_SCHEMA = Map({
    'name': Str(),
    'url': Url(),
})


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    CourseProvider.drop_table()
    CourseProvider.create_table()

    for yaml_path in YAML_DIR_PATH.glob('*.yml'):
        logger.info(yaml_path.name)
        yaml_record = load(yaml_path.read_text(), YAML_SCHEMA)
        record = yaml_record.data
        record['slug'] = yaml_path.stem
        CourseProvider.create(**record)
