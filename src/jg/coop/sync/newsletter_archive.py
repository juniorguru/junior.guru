import json
import re
from datetime import date, datetime
from pathlib import Path

import click

from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.lib.text import remove_emoji
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

            title = remove_emoji(item["subject"])
            body = process_body(item["body"])

            content = f"""---
title: {json.dumps(title, ensure_ascii=False)}
description: Začínáš v IT? V tomhle newsletteru najdeš pozvánky, kurzy, podcasty, přednášky, články a další zdroje, které tě posunou a namotivují.
date: {published_on}
thumbnail_title: {title}
thumbnail_subheading: Newsletter
thumbnail_date: {published_on}
thumbnail_button_heading: Čti na
thumbnail_button_link: junior.guru/news
template: main_subnav.html
---

{{% from 'macros.html' import lead with context %}}

# {title}

{{% call lead() %}}
Prohrabáváš se archivem zdejšího newsletteru a koukáš na jedno ze starších vydání.
Pokud chceš, aby ti takové e-maily chodily čerstvé, [přihlaš se k odebírání](../news.jinja)!
{{% endcall %}}

<div class="newsletter-issue">
<p class="newsletter-issue-date">Odesláno {published_on:%-d.%-m.%Y}</p>
{body}
</div>

<div class="pagination">
  <div class="pagination-control">
    <a href="{{{{ (page|parent_page).url|url }}}}" class="pagination-button">
      {{{{ 'arrow-left'|icon }}}}
      Všechna vydání
    </a>
  </div>
</div>
"""
            path = pages_dir / f"{item['slug']}.md"
            path.write_text(content)
            logger.info(f"Archived as {path}")

            # TODO canonical_url, image


def process_body(body: str) -> str:
    # remove double <br>
    body = re.sub(r"<br>\s*<br>", "<br>", body)

    # strip emoji from <h2> and <h3>
    body = re.sub(r"(<h2[^>]*>)(.*?)(</h2>)", _strip_emoji, body)
    body = re.sub(r"(<h3[^>]*>)(.*?)(</h3>)", _strip_emoji, body)

    return body


def _strip_emoji(match: re.Match) -> str:
    return f"{match.group(1)}{remove_emoji(match.group(2))}{match.group(3)}"
