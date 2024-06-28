from datetime import date, timedelta
from functools import wraps
from pathlib import Path
from typing import Callable

import requests
import yaml
from pydantic import HttpUrl

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.sponsor import Sponsor


YAML_DIR_PATH = Path("jg/coop/data/course_providers")

STRING_LENGTH_SEO_LIMIT = 150


logger = loggers.from_path(__file__)


class CourseProviderConfig(YAMLConfig):
    name: str
    url: HttpUrl
    usp_description: str | None = None
    questions: list[str] | None = None
    cz_business_id: int | None = None


@cli.sync_command(dependencies=["sponsors"])
@db.connection_context()
def main():
    CourseProvider.drop_table()
    CourseProvider.create_table()

    for yaml_path in YAML_DIR_PATH.glob("*.yml"):
        logger.info(f"Reading {yaml_path.name}")
        yaml_data = yaml.safe_load(yaml_path.read_text())
        config = CourseProviderConfig(**yaml_data)
        slug = yaml_path.stem
        try:
            sponsor = Sponsor.get_by_slug(slug)
        except Sponsor.DoesNotExist:
            logger.debug(f"Course provider {slug!r} is not a sponsor")
            sponsor = None

        CourseProvider.create(
            slug=slug,
            edit_url=(
                "https://github.com/juniorguru/junior.guru/"
                f"blob/main/jg/coop/data/course_providers/{slug}.yml"
            ),
            page_title=compile_page_title(config.name),
            page_description=compile_page_description(config.name, config.questions),
            page_lead=compile_page_lead(config.name, config.questions),
            sponsor=sponsor,
            **config.model_dump(),
        )
        logger.info(f"Loaded {yaml_path.name} as {config.name!r}")

    logger.info("Fetching analytics")
    params = dict(
        version=5,
        fields="pageviews,pages",
        info="false",
        page="/courses/*",
        start=str(date.today() - timedelta(days=365)),
    )
    response = requests.get(
        "https://simpleanalytics.com/junior.guru.json", params=params
    )
    response.raise_for_status()
    data = response.json()
    for page in data["pages"]:
        slug = page["value"].replace("/courses/", "")
        try:
            course_provider = CourseProvider.get_by_slug(slug)
            monthly_pageviews = int(page["pageviews"] / 12)
            course_provider.page_monthly_pageviews = monthly_pageviews
            course_provider.save()
            logger.info(f"Saved {monthly_pageviews} pageviews of {slug!r}")
        except CourseProvider.DoesNotExist:
            logger.warning(f"Course provider {slug!r} not found in the database")


def raise_if_too_long(fn: Callable[..., str]) -> Callable[..., str]:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> str:
        s = fn(*args, **kwargs)
        if len(s) > STRING_LENGTH_SEO_LIMIT:
            raise ValueError(
                f"Return value of {fn.__name__}() has {len(s)} characters, limit is {STRING_LENGTH_SEO_LIMIT}: {s!r}"
            )
        return s

    return wrapper


@raise_if_too_long
def compile_page_title(name: str) -> str:
    if name.lower().startswith("s"):
        return f"Zkušenosti se {name}"
    return f"Zkušenosti s {name}"


@raise_if_too_long
def compile_page_description(name: str, extra_questions: list = None) -> str:
    questions = [
        f"Vyplatí se kurzy programování u {name}?",
        "Co říkají absolventi?",
        "Je to vhodné jako rekvalifikace?",
    ]
    if extra_questions:
        questions += extra_questions
    return " ".join(questions)


@raise_if_too_long
def compile_page_lead(name: str, extra_questions: list = None) -> str:
    questions = [
        f"Vyplatí se {name}?",
        "Hledáš někoho, kdo má zkušenosti?",
        "Je to vhodné jako rekvalifikace?",
    ]
    if extra_questions:
        questions += extra_questions
    return " ".join(questions)
