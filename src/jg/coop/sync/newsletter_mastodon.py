from datetime import date, timedelta

import click
import httpx
from mastodon import Mastodon

from jg.coop.cli.sync import default_from_env, main as cli
from jg.coop.lib import loggers
from jg.coop.lib.mutations import mutating_mastodon
from jg.coop.models.base import db
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["pages"])
@click.option(
    "--today",
    default=lambda: date.today().isoformat(),
    type=date.fromisoformat,
)
@click.option("--server-url", default="https://mastodonczech.cz")
@click.option("--history-limit", default=300, type=int)
@click.option("--client-id", default=default_from_env("MASTODON_CLIENT_ID"))
@click.option("--client-secret", default=default_from_env("MASTODON_CLIENT_SECRET"))
@click.option("--access-token", default=default_from_env("MASTODON_ACCESS_TOKEN"))
@db.connection_context()
def main(
    today: date,
    server_url: str,
    history_limit: int,
    client_id: str | None = None,
    client_secret: str | None = None,
    access_token: str | None = None,
) -> None:
    logger.info("Checking published and archived newsletters")
    newsletter = NewsletterIssue.latest()
    logger.info(f"Latest newsletter URL: {newsletter.absolute_url}")
    try:
        logger.info("Verifying newsletter page accessibility")
        response = httpx.head(newsletter.absolute_url, timeout=5.0)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.warning(f"Newsletter page not accessible: {e}")
    else:
        logger.info(f"Newsletter published on: {newsletter.published_on}")
        if newsletter.published_on >= (today - timedelta(days=60)):
            logger.info("Newsletter is recent enough!")
            mastodon = Mastodon(
                api_base_url=server_url,
                client_id=client_id,
                client_secret=client_secret,
                access_token=access_token,
            )
            account_id = mastodon.me()["id"]
            for status in mastodon.pagination_iterator(
                mastodon.account_statuses(
                    account_id,
                    limit=history_limit,
                    exclude_replies=True,
                    exclude_reblogs=True,
                )
            ):
                if newsletter.absolute_url in status["content"]:
                    logger.info("Newsletter already announced on Mastodon, skipping")
                    return
                logger.debug(f"Checked status {status['url']} ({status['created_at']})")
            logger.info("Announcing newsletter on Mastodon")
            with mutating_mastodon(mastodon) as proxy:
                proxy.status_post(
                    (
                        f"Nový #juniorguru newsletter je venku! "
                        f"„{newsletter.subject}” je k přečtení tady: "
                        f"{newsletter.absolute_url} ({newsletter.reading_time} min čtení)"
                    ),
                    language="cs",
                    idempotency_key=newsletter.absolute_url,
                )
        else:
            logger.warning("Latest newsletter not recent enough")
