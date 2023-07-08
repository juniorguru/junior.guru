from functools import wraps
from pathlib import Path
from typing import Callable

from strictyaml import Int, Map, Optional, Seq, Str, Url, load

from juniorguru.cli.sync import main as cli
from juniorguru.lib import loggers
from juniorguru.models.base import db
from juniorguru.models.course_provider import CourseProvider
from juniorguru.models.partner import Partner


YAML_DIR_PATH = Path('juniorguru/data/course_providers')

YAML_SCHEMA = Map({
    'name': Str(),
    'url': Url(),
    Optional('questions'): Seq(Str()),
    Optional('cz_business_id'): Int(),
})

STRING_LENGTH_SEO_LIMIT = 150


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=['partners'])
@db.connection_context()
def main():
    CourseProvider.drop_table()
    CourseProvider.create_table()

    for yaml_path in YAML_DIR_PATH.glob('*.yml'):
        logger.info(f'Reading {yaml_path.name}')
        yaml_record = load(yaml_path.read_text(), YAML_SCHEMA)
        record = yaml_record.data

        record['slug'] = yaml_path.stem
        record['edit_url'] = ('https://github.com/honzajavorek/junior.guru/'
                              f"blob/main/juniorguru/data/course_providers/{record['slug']}.yml")
        record['page_title'] = compile_page_title(record['name'])
        record['page_description'] = compile_page_description(record['name'], record.get('questions'))
        record['page_lead'] = compile_page_lead(record['name'], record.get('questions'))
        record['partner'] = Partner.first_by_slug(record['slug'])

        CourseProvider.create(**record)
        logger.info(f'Loaded {yaml_path.name} as {record["name"]!r}')


def raise_if_too_long(fn: Callable[..., str]) -> Callable[..., str]:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> str:
        s = fn(*args, **kwargs)
        if len(s) > STRING_LENGTH_SEO_LIMIT:
            raise ValueError(f'Return value of {fn.__name__}() has {len(s)} characters, limit is {STRING_LENGTH_SEO_LIMIT}: {s!r}')
        return s
    return wrapper


@raise_if_too_long
def compile_page_title(name: str) -> str:
    if name.lower().startswith('s'):
        return f'Zkušenosti se {name}'
    return f'Zkušenosti s {name}'


@raise_if_too_long
def compile_page_description(name: str, extra_questions: list=None) -> str:
    questions = [f'Vyplatí se kurzy programování u {name}?',
                 'Co říkají absolventi?',
                 'Je to vhodné jako rekvalifikace?']
    if extra_questions:
        questions += extra_questions
    return ' '.join(questions)


@raise_if_too_long
def compile_page_lead(name: str, extra_questions: list=None) -> str:
    questions = [f'Vyplatí se {name}?',
                 'Hledáš někoho, kdo má zkušenosti?',
                 'Je to vhodné jako rekvalifikace?']
    if extra_questions:
        questions += extra_questions
    return ' '.join(questions)
