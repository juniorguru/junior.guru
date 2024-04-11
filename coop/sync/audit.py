import click
from github import Auth, Github

from coop.cli.sync import default_from_env, main as cli
from coop.lib import loggers


logger = loggers.from_path(__file__)


@cli.sync_command()
@click.option(
    "--github-api-key", default=default_from_env("GITHUB_API_KEY"), required=True
)
def main(github_api_key: str):
    client = Github(auth=Auth.Token(github_api_key))
    user = client.get_user(login="PetrValenta92")  # https://github.com/PetrValenta92
    print(user.raw_data)
