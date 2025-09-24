from collections import Counter
from pathlib import Path
from sqlite3 import OperationalError
from typing import Iterable

import click
from diskcache.core import DBNAME
from sqlite_utils import Database

from jg.coop.lib import loggers
from jg.coop.lib.cache import CACHE_DIR, get_cache


logger = loggers.from_path(__file__)


@click.group()
def main():
    pass


@main.command()
def tags():
    try:
        counter = Counter(get_tags(get_db()))
        for tag, count in sorted(counter.items()):
            click.echo(f"{count:10} {tag}")
    except OperationalError:
        pass  # no cache, no output


@main.command()
@click.argument("tag")
@click.pass_context
def clear(context, tag):
    known_tags = frozenset(get_tags(get_db()))
    if tag not in known_tags:
        raise click.BadParameter(
            f"Unknown tag {tag} (known tags: {', '.join(known_tags)})"
        )
    cache = get_cache()
    cache.evict(tag)
    cache.close()
    context.invoke(tags)


@main.command()
def fix():
    cache = get_cache()
    cache.check(fix=True)
    cache.close()


def get_db() -> Database:
    return Database(Path(CACHE_DIR) / DBNAME)


def get_tags(db: Database) -> Iterable[str]:
    for row in db["Cache"].rows_where("tag IS NOT NULL"):
        yield row["tag"]
