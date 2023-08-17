from collections import Counter
from pathlib import Path
from typing import Any, Callable, Generator

import mkdocs_gen_files
from strictyaml import as_document

from juniorguru.lib import loggers
from juniorguru.models.course_provider import CourseProvider
from juniorguru.models.event import Event
from juniorguru.models.partner import Partnership
from juniorguru.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


TEMPLATES_DIR = Path("juniorguru/web/docs_templates")

TEMPLATES = {}


def template(generate_pages: Callable) -> Callable:
    TEMPLATES[generate_pages.__name__] = generate_pages
    return generate_pages


@template
def generate_event_pages() -> Generator[dict[str, Any], None, None]:
    for event in Event.listing():
        yield dict(
            path=f"events/{event.id}.md",
            meta=dict(
                title=event.title,
                # description=event.page_description,  # TODO
                event_id=event.id,
            ),
            template="event.md",
        )


@template
def generate_podcast_episode_pages() -> Generator[dict[str, Any], None, None]:
    for podcast_episode in PodcastEpisode.listing():
        yield dict(
            path=f"podcast/{podcast_episode.number}.jinja",
            meta=dict(
                title=podcast_episode.title,
                # description=event.page_description,  # TODO
                podcast_episode_number=podcast_episode.number,
            ),
            template="podcast_episode.jinja",
        )


@template
def generate_course_provider_pages() -> Generator[dict[str, Any], None, None]:
    for course_provider in CourseProvider.listing():
        yield dict(
            path=f"courses/{course_provider.slug}.md",
            meta=dict(
                title=course_provider.page_title,
                description=course_provider.page_description,
                course_provider_slug=course_provider.slug,
                topic_name=course_provider.slug,
            ),
            template="course_provider.md",
        )


@template
def generate_partner_pages() -> Generator[dict[str, Any], None, None]:
    for partnership in Partnership.active_listing():
        partner = partnership.partner
        yield dict(
            path=f"open/{partner.slug}.md",
            meta=dict(
                title=f"Partnerství s firmou {partner.name}",
                partner_slug=partner.slug,
                noindex=True,
            ),
            template="partner.md",
        )


def main():
    logger.info("Generating pages")
    counter = Counter()
    for name, generate_pages in TEMPLATES.items():
        logger[name].debug("Generating")
        for page in generate_pages():
            path = page["path"]
            yaml = as_document(page["meta"]).as_yaml()
            markdown = (TEMPLATES_DIR / page["template"]).read_text()
            content = f"---\n{yaml}\n---\n{markdown}"
            logger[name].debug(f"Writing {len(content)} characters to {path}")
            with mkdocs_gen_files.open(path, "w") as f:
                f.write(content)
            counter[name] += 1
        level = "info" if counter[name] else "warning"
        getattr(logger[name], level)(f"Generated {counter[name]} pages")


if __name__ in ("__main__", "<run_path>"):
    main()
