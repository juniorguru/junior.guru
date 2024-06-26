from jg.coop.cli.sync import main as cli
from jg.coop.lib import apify, loggers
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseUP


logger = loggers.from_path(__file__)


@cli.sync_command()
@db.connection_context()
def main():
    CourseUP.drop_table()
    CourseUP.create_table()

    for course in (item for item in apify.fetch_data("honzajavorek/courses-up")):
        logger.info(f'Saving {course["name"]!r}')
        CourseUP.create(**course)

    logger.info(f"Saved {CourseUP.count()} courses in total")
