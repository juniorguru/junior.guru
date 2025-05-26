from collections import Counter
from pathlib import Path
from typing import Any, Generator

import mkdocs_gen_files
from mkdocs.utils.meta import get_data as parse_document
from pydantic import BaseModel, ConfigDict
from slugify import slugify
from strictyaml import as_document

from jg.coop.lib import loggers
from jg.coop.lib.mapycz import REGIONS
from jg.coop.lib.text import get_tag_slug
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


DOCS_DIR = Path("jg/coop/web/generated_docs")


class GeneratedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str | Path
    meta: dict[str, Any] = {}
    content: str

    def __str__(self) -> str:
        yaml = as_document(self.meta).as_yaml()
        return f"---\n{yaml}\n---\n{self.content}"


def generate_redirects() -> Generator[GeneratedDocument, None, None]:
    for path, redirect in [
        ("candidate-handbook.md", "handbook/candidate.md"),
        ("donate.md", "love.jinja"),
        ("hire-juniors.md", "love.jinja"),
        ("jobs/austria.md", "jobs.jinja"),
        ("jobs/germany.md", "jobs.jinja"),
        ("jobs/poland.md", "jobs.jinja"),
        ("jobs/region/brno.md", "jobs/brno.jinja"),
        ("jobs/region/ceske-budejovice.md", "jobs/ceske-budejovice.jinja"),
        ("jobs/region/hradec-kralove.md", "jobs/hradec-kralove.jinja"),
        ("jobs/region/jihlava.md", "jobs/jihlava.jinja"),
        ("jobs/region/karlovy-vary.md", "jobs/karlovy-vary.jinja"),
        ("jobs/region/liberec.md", "jobs/liberec.jinja"),
        ("jobs/region/olomouc.md", "jobs/olomouc.jinja"),
        ("jobs/region/ostrava.md", "jobs/ostrava.jinja"),
        ("jobs/region/pardubice.md", "jobs/pardubice.jinja"),
        ("jobs/region/plzen.md", "jobs/plzen.jinja"),
        ("jobs/region/praha.md", "jobs/praha.jinja"),
        ("jobs/region/usti-nad-labem.md", "jobs/usti-nad-labem.jinja"),
        ("jobs/region/zlin.md", "jobs/zlin.jinja"),
        ("jobs/slovakia.md", "jobs.jinja"),
        ("learn.md", "handbook/learn.md"),
        ("motivation.md", "handbook/motivation.md"),
        ("open.md", "about/index.md"),
        ("practice.md", "handbook/practice.md"),
        ("pricing.md", "love.jinja"),
        ("press/index.md", "about/index.md"),
        ("press/crisis.md", "about/index.md"),
        ("press/handbook.md", "about/handbook.md"),
        ("press/women.md", "about/women.md"),
        ("sponsorship.md", "love.jinja"),
        ("topics/codingbootcamppraha.md", "courses/codingbootcamppraha.md"),
        ("topics/cs50.md", "courses/cs50.md"),
        ("topics/czechitas.md", "courses/czechitas.md"),
        ("topics/djangogirls.md", "courses/djangogirls.md"),
        ("topics/engeto.md", "courses/engeto.md"),
        ("topics/git.md", "handbook/git.md"),
        ("topics/github.md", "handbook/git.md"),
        ("topics/greenfox.md", "courses/greenfox.md"),
        ("topics/itnetwork.md", "courses/itnetwork.md"),
        ("topics/learn2code.md", "courses/skillmea.md"),
        ("topics/primakurzy.md", "courses/primakurzy.md"),
        ("topics/pyladies.md", "courses/pyladies.md"),
        ("topics/reactgirls.md", "courses/reactgirls.md"),
        ("topics/sdacademy.md", "courses/sdacademy.md"),
        ("topics/skillmea.md", "courses/skillmea.md"),
        ("topics/step.md", "courses/step.md"),
        ("topics/udemy.md", "courses/udemy.md"),
        ("topics/unicorn.md", "courses/unicornhatchery.md"),
        ("topics/vsb.md", "courses/kurzyvsb.md"),
    ]:
        yield GeneratedDocument(
            path=path,
            meta=dict(
                title="Přesměrování",
                template="redirect.html",
                redirect=redirect,
            ),
            content=(DOCS_DIR / "redirect.jinja").read_text(),
        )


def generate_job_pages() -> Generator[GeneratedDocument, None, None]:
    jobs_file = Path("jg/coop/web/docs/jobs.jinja")
    jobs_text = jobs_file.read_text(encoding="utf-8-sig", errors="strict")
    content, meta = parse_document(jobs_text)
    for region in REGIONS:
        doc_slug = slugify(region)
        tag_slug = get_tag_slug(region)
        yield GeneratedDocument(
            path=f"jobs/{doc_slug}.jinja",
            meta=meta | dict(
                title=f"{meta['title']}: {region}",
                description=f"Jaké nabízí {region} příležitosti pro začátečníky v IT? {meta['description']}",
                region=region,
                region_tag_slug=tag_slug,
            ),
            content=content,
        )


def generate_event_pages() -> Generator[GeneratedDocument, None, None]:
    for event in Event.listing():
        yield GeneratedDocument(
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
            content=(DOCS_DIR / "event.md").read_text(),
        )


def generate_podcast_episode_pages() -> Generator[GeneratedDocument, None, None]:
    for podcast_episode in PodcastEpisode.listing():
        yield GeneratedDocument(
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
            content=(DOCS_DIR / "podcast_episode.jinja").read_text(),
        )


def generate_course_provider_pages() -> Generator[GeneratedDocument, None, None]:
    for course_provider in CourseProvider.listing():
        yield GeneratedDocument(
            path=f"courses/{course_provider.slug}.md",
            meta=dict(
                title=course_provider.page_title,
                description=course_provider.page_description,
                course_provider_slug=course_provider.slug,
                topic_name=course_provider.slug,
            ),
            content=(DOCS_DIR / "course_provider.md").read_text(),
        )


def main():
    generators = [
        generate_redirects,
        generate_job_pages,
        generate_event_pages,
        generate_podcast_episode_pages,
        generate_course_provider_pages,
    ]
    logger.info(f"Generating documents ({len(generators)} generators)")
    counter = Counter()
    for generator in generators:
        name = generator.__name__
        logger[name].debug("Generating")
        for document in generator():
            logger[name].debug(f"Writing to {document.path}")
            with mkdocs_gen_files.open(document.path, "w") as f:
                f.write(str(document))
            counter[name] += 1
        level = "info" if counter[name] else "warning"
        getattr(logger[name], level)(f"Generated {counter[name]} documents")


if __name__ in ("__main__", "<run_path>"):
    main()
