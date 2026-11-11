import click

from jg.coop.lib.memberful import (
    MEMBERFUL_EMAIL,
    MEMBERFUL_PASSWORD,
    acquire_trusted_browser,
)


@click.command()
@click.option("--email", default=MEMBERFUL_EMAIL, show_default=True)
@click.password_option(
    "--password",
    default=MEMBERFUL_PASSWORD,
    confirmation_prompt=False,
    help="Defaults to MEMBERFUL_PASSWORD, otherwise prompts",
)
def main(email: str, password: str):
    """Sign into Memberful with a one-time code and print the value for MEMBERFUL_TRUSTED_BROWSER"""
    value = acquire_trusted_browser(
        email,
        password,
        lambda: click.prompt(f"One-time code Memberful sent to {email}").strip(),
    )
    click.echo(
        "Set this as MEMBERFUL_TRUSTED_BROWSER in CircleCI project settings:",
        err=True,
    )
    click.echo(value)
