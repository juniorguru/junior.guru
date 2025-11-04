from datetime import date, datetime
import json
from pathlib import Path
from textwrap import dedent

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.models.base import db


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--pages-dir",
    default=Path("src/jg/coop/web/docs/news"),
    type=click.Path(path_type=Path, file_okay=False, writable=True),
)
@click.option(
    "--today", default=lambda: date.today().isoformat(), type=date.fromisoformat
)
@db.connection_context()
@async_command
async def main(pages_dir: Path, today: date):
    async with ButtondownAPI() as api:
        async for item in api.get_emails_before(today):
            published_on = datetime.fromisoformat(item["publish_date"]).date()
            logger.info(f"Email published on {published_on}: {item['absolute_url']}")

            content = dedent(
                f"""
                    ---
                    title: {json.dumps(item["subject"], ensure_ascii=False)}
                    date: {published_on.isoformat()}
                    thumbnail_button_heading: Čti na
                    thumbnail_button_link: junior.guru/news
                    ---

                    # {item["subject"]}
                """
            ).strip() + "\n\n" + item["body"]

            path = pages_dir / f"{item['slug']}.md"
            path.write_text(content)
            logger.info(f"Archived as {path}")

            # TODO canonical_url, image
