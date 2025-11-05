from jg.coop.cli.sync import main as cli
from jg.coop.lib import loggers
from jg.coop.lib.buttondown import ButtondownAPI
from jg.coop.lib.cli import async_command
from jg.coop.models.base import db
from jg.coop.models.newsletter import NewsletterIssue


logger = loggers.from_path(__file__)


@cli.sync_command(dependencies=["thumbnails"])
@db.connection_context()
@async_command
async def main():
    async with ButtondownAPI() as api:
        for newsletter_issue in NewsletterIssue.listing():
            logger_ni = logger[newsletter_issue.buttondown_id]
            if updates := newsletter_issue.get_buttondown_updates():
                logger_ni.info(f"Updating with: {updates!r}")
                await api.update_email(newsletter_issue.buttondown_id, updates)
            else:
                logger_ni.info("No updates needed")
