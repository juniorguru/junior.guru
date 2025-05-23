from collections import Counter
from pathlib import Path
from typing import Any, Callable, Generator

import mkdocs_gen_files
from strictyaml import as_document

from jg.coop.lib import loggers
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


TEMPLATES_DIR = Path("jg/coop/web/docs_templates")

TEMPLATES = {}


def template(generate_pages: Callable) -> Callable:
    TEMPLATES[generate_pages.__name__] = generate_pages
    return generate_pages


@template
def generate_redirects() -> Generator[dict[str, Any], None, None]:
    for path, redirect in [
        ("motivation.md", "handbook/motivation.md"),
        ("learn.md", "handbook/learn.md"),
        ("practice.md", "handbook/practice.md"),
        ("candidate-handbook.md", "handbook/candidate.md"),
        ("topics/git.md", "handbook/git.md"),
        ("topics/github.md", "handbook/git.md"),
        ("topics/codingbootcamppraha.md", "courses/codingbootcamppraha.md"),
        ("topics/cs50.md", "courses/cs50.md"),
        ("topics/czechitas.md", "courses/czechitas.md"),
        ("topics/djangogirls.md", "courses/djangogirls.md"),
        ("topics/engeto.md", "courses/engeto.md"),
        ("topics/greenfox.md", "courses/greenfox.md"),
        ("topics/itnetwork.md", "courses/itnetwork.md"),
        ("topics/learn2code.md", "courses/skillmea.md"),
        ("topics/primakurzy.md", "courses/primakurzy.md"),
        ("topics/pyladies.md", "courses/pyladies.md"),
        ("topics/reactgirls.md", "courses/reactgirls.md"),
        ("topics/sdacademy.md", "courses/sdacademy.md"),
        ("topics/step.md", "courses/step.md"),
        ("topics/udemy.md", "courses/udemy.md"),
        ("topics/unicorn.md", "courses/unicornhatchery.md"),
        ("topics/vsb.md", "courses/kurzyvsb.md"),
        ("topics/skillmea.md", "courses/skillmea.md"),
        ("donate.md", "love.jinja"),
        ("hire-juniors.md", "love.jinja"),
        ("pricing.md", "love.jinja"),
        ("sponsorship.md", "love.jinja"),
        ("open.md", "about/index.md"),
    ]:
        yield dict(
            path=path,
            meta=dict(
                title="Přesměrování",
                template="redirect.html",
                redirect=redirect,
            ),
            template="redirect.jinja",
        )


@template
def generate_event_pages() -> Generator[dict[str, Any], None, None]:
    for event in Event.listing():
        yield dict(
            path=f"events/{event.id}.md",
            meta=dict(
                title=f"{event.full_title} – online akce na Discordu junior.guru",
                description=(
                    "Klub junior.guru pořádá vzdělávací akce, online na svém Discordu. "
                    "Mohou to být přednášky, stream, Q&A, AMA, webináře… "
                    "Toto je stránka o jedné z nich."
                ),
                template="main_subnav.html",
                event_id=event.id,
                **event.to_thumbnail_meta(),
            ),
            template="event.md",
        )


@template
def generate_podcast_episode_pages() -> Generator[dict[str, Any], None, None]:
    for podcast_episode in PodcastEpisode.listing():
        yield dict(
            path=f"podcast/{podcast_episode.number}.jinja",
            meta=dict(
                title=f"Podcast – {podcast_episode.format_title()}",
                description=f"Poslechni si {podcast_episode.number}. díl Junior Guru podcastu.",
                podcast_episode_number=podcast_episode.number,
                thumbnail_title=podcast_episode.format_title(affiliation=False),
                thumbnail_subheading=f"Epizoda {podcast_episode.number}",
                thumbnail_image_path=podcast_episode.image_path,
                thumbnail_button_heading="Poslouchej na",
                thumbnail_button_link="junior.guru/podcast",
                thumbnail_platforms=["youtube", "spotify", "apple"],
                template="main_subnav.html",
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
