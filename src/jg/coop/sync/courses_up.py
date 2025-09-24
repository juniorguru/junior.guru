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

    courses_with_issues = []
    for course in apify.fetch_data("honzajavorek/courses-up"):
        logger.info(f"Saving {course['name']!r}")
        if course["description"] is None:
            courses_with_issues.append(course)
        else:
            course["business_id"] = int(course["business_id"].lstrip("0"))
            CourseUP.add(**course)

    if courses_with_issues:
        for course in courses_with_issues:
            logger.warning(f"Course {course!r} has issues.")
        logger.warning(f"Skipped {len(courses_with_issues)} courses in total.")

    logger.info(f"Saved {CourseUP.count()} courses in total.")
