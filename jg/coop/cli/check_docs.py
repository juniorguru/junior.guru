from pathlib import Path

import click
from lxml import html

from jg.coop.cli.web import build as build_web
from jg.coop.lib import loggers


logger = loggers.from_path(__file__)


class EmailLinkError(ValueError):
    pass


class WebCalLinkError(ValueError):
    pass


class ExternalLinkError(ValueError):
    pass


class StaticFileLinkError(ValueError):
    pass


@click.command()
@click.argument(
    "output_path", default="public", type=click.Path(exists=True, path_type=Path)
)
@click.option("--build/--no-build", default=True)
@click.pass_context
def main(context, output_path, build):
    if build:
        context.invoke(build_web, output_path=output_path)

    links = []
    targets = set()
    static = set()

    for doc_path in output_path.glob("**/*.html"):
        logger.info(f"Reading {doc_path}")
        doc_name = get_doc_name(output_path, doc_path)
        targets.add(doc_name)

        html_tree = html.fromstring(doc_path.read_bytes())
        for element in html_tree.cssselect("a[name]"):
            targets.add(f"{doc_name}#{element.get('name')}")
        for element in html_tree.cssselect("*[id]"):
            targets.add(f"{doc_name}#{element.get('id')}")
        for element in html_tree.cssselect("a[href]"):
            href = element.get("href")
            try:
                links.append((doc_name, normalize_link(output_path, doc_path, href)))
            except StaticFileLinkError:
                static.add(
                    (doc_name, normalize_static_link(output_path, doc_path, href))
                )
            except ValueError:
                logger.debug(f"Skipping: {href}")
        for element in html_tree.cssselect("img[src]"):
            src = element.get("data-src", element.get("src"))
            try:
                static.add(
                    (doc_name, normalize_static_link(output_path, doc_path, src))
                )
            except ValueError:
                logger.debug(f"Skipping: {src}")

    broken = False
    for doc_name, link in links:
        if link not in targets:
            logger.error(f"Broken link! {doc_name} links to {link}")
            broken = True
    for doc_name, static_path in static:
        static_path = output_path / static_path
        if not static_path.exists():
            logger.error(f"Broken static file! {doc_name} links to {static_path}")
            broken = True
    if broken:
        raise click.Abort()
    else:
        logger.info(
            f"Checked {len(links)} links, {len(targets)} targets, {len(static)} static files. All good!"
        )


def get_doc_name(output_path, doc_path):
    doc_name = f"/{doc_path.relative_to(output_path)}"
    if doc_name.endswith("index.html"):
        return doc_name[:-10]
    return doc_name


def normalize_link(output_path, doc_path, link):
    if link.startswith("http"):
        raise ExternalLinkError(link)
    if link.startswith("mailto"):
        raise EmailLinkError(link)
    if link.startswith("webcal"):
        raise WebCalLinkError(link)
    if Path(link.split("#")[0]).suffix not in ("", ".md"):
        raise StaticFileLinkError(link)
    if link.startswith("#"):
        link = f"{get_doc_name(output_path, doc_path)}{link}"
    if not link.startswith((".", "/")):
        link = f"./{link}"
    if link.startswith("."):
        link = f"/{doc_path.parent.joinpath(link).resolve().relative_to(output_path.absolute())}"
    if not link.endswith("/") and "#" not in link:
        link = f"{link}/"
    if link == "/./":
        link = "/"
    return link


def normalize_static_link(output_path, doc_path, link):
    if link.startswith("http"):
        raise ExternalLinkError(link)
    if link.startswith("mailto"):
        raise EmailLinkError(link)
    if link.startswith("/"):
        return link.lstrip("/")
    if link.startswith("."):
        return f"{doc_path.parent.joinpath(link).resolve().relative_to(output_path.absolute())}"
    return link
