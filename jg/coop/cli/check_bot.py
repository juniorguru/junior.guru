import click
import requests

from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


@click.command()
@click.option("--bot-url", default="https://juniorguru-chick.fly.dev")
def main(bot_url):
    response = requests.get(bot_url)
    response.raise_for_status()
    data = response.json()
    if data["status"] == "ok":
        logger.info(
            f"Bot is up! Uptime {data['uptime_sec']}s ({data['uptime_sec'] / 60:.1f}min, {data['uptime_sec'] / 60 / 60:.1f}h, {data['uptime_sec'] / 60 / 60 / 24:.1f}d)"
        )
    else:
        raise ValueError(f"Unexpected status: {data['status']}")
