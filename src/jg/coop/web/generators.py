from collections import Counter
from pathlib import Path
from typing import Any, Generator

import mkdocs_gen_files
import yaml
from mkdocs.utils.meta import get_data as parse_document
from pydantic import BaseModel, ConfigDict
from slugify import slugify
from strictyaml import as_document

from jg.coop.lib import loggers
from jg.coop.lib.location import REGIONS
from jg.coop.lib.text import get_tag_slug
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.job import REMOTE_TAG_SLUG, ListedJob
from jg.coop.models.newsletter import NewsletterIssue
from jg.coop.models.podcast import PodcastEpisode


logger = loggers.from_path(__file__)


REDIRECTS_YAML_PATH = Path("src/jg/coop/data/redirects.yml")

DOCS_DIR = Path("src/jg/coop/web/generated_docs")


class GeneratedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str | Path
    meta: dict[str, Any] = {}
    content: str

    def __str__(self) -> str:
        yaml = as_document(self.meta).as_yaml()
        return f"---\n{yaml}\n---\n{self.content}"


class RedirectConfig(YAMLConfig):
    from_url: str
    to_doc: str

    @property
    def from_doc(self) -> str:
        return self.from_url.strip("/") + "/index.md"


class RedirectsConfig(YAMLConfig):
    registry: list[RedirectConfig]


def generate_redirects() -> Generator[GeneratedDocument, None, None]:
    config = RedirectsConfig(**yaml.safe_load(REDIRECTS_YAML_PATH.read_text()))
    for redirect in config.registry:
        yield GeneratedDocument(
            path=redirect.from_doc,
            meta=dict(
                title="Přesměrování",
                template="redirect.html",
                redirect=redirect.to_doc,
            ),
            content=(DOCS_DIR / "redirect.jinja").read_text(),
        )


def generate_region_jobs_pages() -> Generator[GeneratedDocument, None, None]:
    jobs_file = Path("src/jg/coop/web/docs/jobs.jinja")
    jobs_text = jobs_file.read_text(encoding="utf-8-sig", errors="strict")
    content, meta = parse_document(jobs_text)
    yield GeneratedDocument(
        path=f"jobs/{REMOTE_TAG_SLUG}.jinja",
        meta=meta
        | dict(
            title=f"{meta['title']}: na dálku, z domova, remote",
            description=(
                "Pracovní příležitosti pro začátečníky v IT, "
                f"které jsou na dálku, z domova, remote. {meta['description']}"
            ),
            region="na dálku",
            region_tag_slug=REMOTE_TAG_SLUG,
        ),
        content=content,
    )
    for region in REGIONS:
        doc_slug = slugify(region)
        tag_slug = get_tag_slug(region)
        yield GeneratedDocument(
            path=f"jobs/{doc_slug}.jinja",
            meta=meta
            | dict(
                title=f"{meta['title']}: {region}",
                description=f"Jaké nabízí {region} příležitosti pro začátečníky v IT? {meta['description']}",
                region=region,
                region_tag_slug=tag_slug,
            ),
            content=content,
        )


@db.connection_context()
def generate_job_pages() -> Generator[GeneratedDocument, None, None]:
    for job in ListedJob.submitted_listing():
        yield GeneratedDocument(
            path=f"jobs/{job.submitted_job.id}.jinja",
            meta=dict(
                title=f"{job.title_short} – {job.company_name} – {job.location_text or '?'}",
                description=(
                    f"Pracovní nabídka pro začínající programátory: "
                    f"{job.title} – {job.company_name}, {job.location_text or '?'}"
                ),
                job_id=job.submitted_job.id,
                template="main_subnav.html",
            ),
            content=(DOCS_DIR / "job.jinja").read_text(),
        )


@db.connection_context()
def generate_event_pages() -> Generator[GeneratedDocument, None, None]:
    for event in Event.listing():
        if event.venue:
            title_suffix = "junior.guru akce"
            description = (
                "Klub junior.guru pořádá vzdělávací akce. "
                "Mohou to být přednášky, workshopy, konference… "
                "Toto je stránka o jedné z nich."
            )
        else:
            title_suffix = "online akce na Discordu junior.guru"
            description = (
                "Klub junior.guru pořádá vzdělávací akce, online na svém Discordu. "
                "Mohou to být přednášky, stream, Q&A, AMA, webináře… "
                "Toto je stránka o jedné z nich."
            )
        yield GeneratedDocument(
            path=f"events/{event.id}.md",
            meta=dict(
                title=f"{event.get_full_title(separator='–')} – {title_suffix}",
                description=description,
                template="main_subnav.html",
                event_id=event.id,
                **event.to_thumbnail_meta(),
            ),
            content=(DOCS_DIR / "event.md").read_text(),
        )


@db.connection_context()
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


@db.connection_context()
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


@db.connection_context()
def generate_newsletter_issue_pages() -> Generator[GeneratedDocument, None, None]:
    for newsletter_issue in NewsletterIssue.listing():
        yield GeneratedDocument(
            path=f"news/{newsletter_issue.slug}.md",
            meta=dict(
                title=newsletter_issue.subject,
                description="Začínáš v IT? V tomhle newsletteru najdeš pozvánky, kurzy, podcasty, přednášky, články a další zdroje, které tě posunou a namotivují.",
                date=newsletter_issue.published_on.isoformat(),
                newsletter_issue_id=newsletter_issue.id,
                template="main_subnav.html",
                thumbnail_title=newsletter_issue.subject,
                thumbnail_subheading="Newsletter",
                thumbnail_date=newsletter_issue.published_on.isoformat(),
                thumbnail_button_heading="Čti na",
                thumbnail_button_link="junior.guru/news",
            ),
            content=(DOCS_DIR / "newsletter_issue.md").read_text(),
        )


def main():
    generators = [
        generate_course_provider_pages,
        generate_event_pages,
        generate_job_pages,
        generate_newsletter_issue_pages,
        generate_podcast_episode_pages,
        generate_redirects,
        generate_region_jobs_pages,
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
