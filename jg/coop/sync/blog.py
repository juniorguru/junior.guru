from datetime import date
from operator import attrgetter

import click
import feedparser
import requests

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.models.base import db
from jg.coop.models.blog import BlogArticle


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option("--feed-url", default="https://honzajavorek.cz/tag/juniorguru.xml")
@db.connection_context()
def main(feed_url: str):
    BlogArticle.drop_table()
    BlogArticle.create_table()

    logger.info(f"Reading feed: {feed_url}")
    response = requests.get(feed_url)
    response.raise_for_status()
    articles = feedparser.parse(response.content).entries
    articles = sorted(articles, key=attrgetter("published"), reverse=True)

    for article in articles:
        logger.info(f"Saving blog article: {article.link}")
        BlogArticle.create(
            title=article.title,
            url=article.link,
            published_on=date(*article.published_parsed[:3]),
        )
