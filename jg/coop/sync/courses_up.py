from datetime import timedelta

import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.cache import cache
from jg.coop.lib.remove_emoji import remove_emoji
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseUP


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    CourseUP.drop_table()
    CourseUP.create_table()

    for course in fetch_courses():
        logger.debug(f'Saving {course["nazev"]!r}')
        CourseUP.create(
            id=course["id"],
            url=f"https://www.uradprace.cz/web/cz/vyhledani-rekvalifikacniho-kurzu#/rekvalifikacni-kurz-detail/{course['id']}",
            name=remove_emoji(course["nazev"]),
            description=course["popisRekvalifikace"],
            cz_business_id=int(course["osoba"]["ico"].lstrip("0")),
        )
    logger.info(f"Saved {CourseUP.count()} courses in total")


@cache(expire=timedelta(days=1), tag="courses-up")
def fetch_courses() -> list[dict]:
    logger.info("Fetching courses")
    courses = []
    start = 0
    step = 100
    while True:
        logger.info(f"Fetching courses from {start} to {start + step}")
        response = requests.post(
            "https://www.uradprace.cz/rekvalifikace/rest/kurz/query",
            json={
                "index": ["rekvalifikace"],
                "pagination": {"start": start, "count": step, "order": ["-id"]},
                "query": {
                    "must": [
                        {
                            "match": {
                                "field": "kategorie.kategorieId",
                                "query": 10115,
                            }
                        },
                    ]
                },
            },
            headers={
                "User-Agent": "JuniorGuruBot (+https://junior.guru)",
            },
        )
        response.raise_for_status()
        response_list = response.json()["list"]
        if response_list:
            courses.extend(response_list)
            start += step
        else:
            break
    logger.info(f"Downloaded {len(courses)} courses in total")
    return courses
