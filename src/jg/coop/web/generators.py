from collections import Counter
from collections.abc import Generator
from pathlib import Path
from typing import Any

import mkdocs_gen_files
import yaml
from mkdocs.utils.meta import get_data as parse_document
from pydantic import BaseModel, ConfigDict

from jg.coop.lib import loggers
from jg.coop.lib.yaml import YAMLConfig
from jg.coop.models.base import db
from jg.coop.models.course_provider import CourseProvider
from jg.coop.models.event import Event
from jg.coop.models.job import ListedJob
from jg.coop.models.jobs_listing import JobsListingPage
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
        meta_yaml = yaml.safe_dump(
            self.meta,
            allow_unicode=True,
            sort_keys=False,
        )
        return f"---\n{meta_yaml.strip()}\n---\n{self.content}"


class RedirectConfig(YAMLConfig):
    from_url: str
    to_doc: str

    @property
    def from_doc(self) -> str:
        return self.from_url.strip("/") + "/index.md"


class RedirectsConfig(YAMLConfig):
    registry: list[RedirectConfig]


def generate_redirects() -> Generator[GeneratedDocument]:
    config = RedirectsConfig(**yaml.safe_load(REDIRECTS_YAML_PATH.read_text()))
    for redirect in config.registry:
        yield GeneratedDocument(
            path=redirect.from_doc,
            meta={
                "title": "Přesměrování",
                "template": "redirect.html",
                "redirect": redirect.to_doc,
            },
            content=(DOCS_DIR / "redirect.jinja").read_text(),
        )


@db.connection_context()
def generate_jobs_listing_pages() -> Generator[GeneratedDocument]:
    jobs_file = Path("src/jg/coop/web/docs/jobs.jinja")
    jobs_text = jobs_file.read_text(encoding="utf-8-sig", errors="strict")
    content, meta = parse_document(jobs_text)
    for listing in JobsListingPage.listing():
        yield GeneratedDocument(
            path=listing.doc_path,
            meta=build_listing_meta(meta, listing),
            content=content,
        )


def build_listing_meta(
    base_meta: dict[str, Any], listing: JobsListingPage
) -> dict[str, Any]:
    """
    Page metadata for a jobs listing page, based on the main jobs page metadata
    """
    return base_meta | {
        "title": listing.title,
        "description": listing.description,
        "jobs_listing_slug": listing.slug,
    }


@db.connection_context()
def generate_job_pages() -> Generator[GeneratedDocument]:
    for job in ListedJob.submitted_listing():
        yield GeneratedDocument(
            path=f"jobs/{job.submitted_job.id}.jinja",
            meta={
                "title": f"{job.title_short} – {job.company_name} – {job.location_text or '?'}",
                "description": (
                    f"Pracovní nabídka pro začínající programátory: "
                    f"{job.title} – {job.company_name}, {job.location_text or '?'}"
                ),
                "job_id": job.submitted_job.id,
                "job_company_name": job.company_name,
                "job_apply_url": job.apply_url or "",
                "job_apply_email": job.apply_email or "",
                "template": "main_job.html",
            },
            content=(DOCS_DIR / "job.jinja").read_text(),
        )


@db.connection_context()
def generate_event_pages() -> Generator[GeneratedDocument]:
    archive_size = Event.count_recording()
    for event in Event.listing():
        yield GeneratedDocument(
            path=f"events/{event.id}.md",
            meta=dict(
                title=event.get_full_title(" –"),
                description=event.get_page_description(),
                template="main_content_detail.html",
                event_id=event.id,
                breadcrumb_parent="Klubové akce",
                breadcrumb_item=event.bio_name,
                comments_heading=(
                    f"Chceš pokládat hostům vlastní dotazy? "
                    f"Využiješ video archiv s {archive_size} záznamy?"
                ),
                **event.to_thumbnail_meta(),
            ),
            content=(DOCS_DIR / "event.md").read_text(),
        )


@db.connection_context()
def generate_podcast_episode_pages() -> Generator[GeneratedDocument]:
    for podcast_episode in PodcastEpisode.listing():
        yield GeneratedDocument(
            path=f"podcast/{podcast_episode.number}.jinja",
            meta={
                "title": f"Podcast – {podcast_episode.format_title()}",
                "description": podcast_episode.page_description,
                "podcast_episode_number": podcast_episode.number,
                "breadcrumb_parent": "Podcast",
                "breadcrumb_item": (
                    podcast_episode.guest_name or f"Epizoda {podcast_episode.number}"
                ),
                "thumbnail_title": podcast_episode.format_title(affiliation=False),
                "thumbnail_subheading": f"Epizoda {podcast_episode.number}",
                "thumbnail_image_path": podcast_episode.image_path,
                "thumbnail_button_heading": "Poslouchej na",
                "thumbnail_button_link": "junior.guru/podcast",
                "thumbnail_platforms": ["youtube", "spotify", "apple"],
                "comments_heading": "Máš otázky? Chceš probrat podobná témata?",
                "template": "main_content_detail.html",
            },
            content=(DOCS_DIR / "podcast_episode.jinja").read_text(),
        )


@db.connection_context()
def generate_course_provider_pages() -> Generator[GeneratedDocument]:
    for course_provider in CourseProvider.listing():
        yield GeneratedDocument(
            path=f"courses/{course_provider.slug}.md",
            meta={
                "title": course_provider.page_title,
                "description": course_provider.page_description,
                "course_provider_slug": course_provider.slug,
                "topic_mention_id": course_provider.slug,
            },
            content=(DOCS_DIR / "course_provider.md").read_text(),
        )


@db.connection_context()
def generate_student_pass_pages() -> Generator[GeneratedDocument]:
    for course_provider in CourseProvider.student_pass_listing():
        yield GeneratedDocument(
            path=course_provider.student_pass_page_url,
            meta=build_student_pass_meta(course_provider.name, course_provider.slug),
            content=(DOCS_DIR / "student_pass.jinja").read_text(),
        )


def build_student_pass_meta(name: str, slug: str) -> dict[str, Any]:
    return {
        "title": f"Propustka do\u00a0klubu pro studenty {name}",
        "description": (
            f"Studenti {name} mají v\u00a0klubu junior.guru "
            "kromě dvou týdnů na\u00a0vyzkoušení ještě měsíc zdarma."
        ),
        "course_provider_slug": slug,
        "noindex": True,
    }


@db.connection_context()
def generate_newsletter_issue_pages() -> Generator[GeneratedDocument]:
    for newsletter_issue in NewsletterIssue.listing():
        yield GeneratedDocument(
            path=f"news/{newsletter_issue.slug}.md",
            meta={
                "title": newsletter_issue.subject,
                "description": newsletter_issue.description,
                "date": newsletter_issue.published_on.isoformat(),
                "newsletter_issue_id": newsletter_issue.id,
                "template": "main_subnav.html",
                "thumbnail_title": newsletter_issue.subject,
                "thumbnail_subheading": "Newsletter",
                "thumbnail_date": newsletter_issue.published_on.isoformat(),
                "thumbnail_button_heading": "Čti na",
                "thumbnail_button_link": "junior.guru/news",
            },
            content=(DOCS_DIR / "newsletter_issue.md").read_text(),
        )


def main():
    generators = [
        generate_course_provider_pages,
        generate_event_pages,
        generate_job_pages,
        generate_jobs_listing_pages,
        generate_newsletter_issue_pages,
        generate_podcast_episode_pages,
        generate_redirects,
        generate_student_pass_pages,
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
