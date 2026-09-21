from datetime import date
from inspect import unwrap
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from discord import ForumTag
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader
from peewee import SqliteDatabase

from jg.coop.models.job import ListedJob, TagType
from jg.coop.sync.jobs_club import TAGS_MAPPING, get_forum_tags, prepare_thread_params
from jg.coop.sync.jobs_tech_tags import main


@pytest.fixture
def tagged_job():
    db = SqliteDatabase(":memory:")
    with (
        db.bind_ctx([ListedJob], bind_refs=False, bind_backrefs=False),
        db.connection_context(),
    ):
        db.create_tables([ListedJob])
        job = ListedJob.create(
            title="Junior developer",
            posted_on=date(2026, 9, 21),
            lang="en",
            description_html="<p>Python, Claude Code, RAG, vibe coding.</p>",
            description_text="Python, Claude Code, RAG, vibe coding.",
            description_discord="Python, Claude Code, RAG, vibe coding.",
            company_name="Example",
            company_logo_path="logos-jobs/unknown.webp",
            url="https://example.com/job",
            tech_tags=["obsolete"],
        )
        # Run only the tagging function against the in-memory database.
        unwrap(main.callback)()
        yield ListedJob.get_by_id(job.id)


def test_tags_survive_storage_and_reach_website_filters(tagged_job):
    expected = ["agenticengineering", "ai", "buildingai", "python", "vibecoding"]
    assert tagged_job.tech_tags == expected
    assert [
        tag.slug for tag in tagged_job.tags if tag.type == TagType.TECHNOLOGY
    ] == expected
    assert [tag.slug for tag in ListedJob.tags_by_type()["technology"]] == expected


def test_website_renders_detailed_ai_tags(tagged_job):
    env = Environment(
        loader=ChoiceLoader(
            [
                DictLoader(
                    {
                        "macros.html": """
                {% macro img() %}{% set ignored = (varargs, kwargs) %}{% endmacro %}
                {% macro lead() %}{{ caller() }}{% endmacro %}
                {% macro note() %}{{ caller() }}{% endmacro %}
                {% macro club_teaser(text) %}{% endmacro %}
            """
                    }
                ),
                FileSystemLoader(Path("src/jg/coop/web/docs")),
            ]
        )
    )
    env.filters.update(
        icon=lambda value: value,
        email_link=lambda value: value,
        url=lambda value: value,
        docs_url=lambda pages, path: path,
        relative_url=lambda value: value,
        nplurals=lambda value, *forms: forms[0],
    )
    html = env.get_template("jobs.jinja").render(
        page={"meta": {}},
        pages=[],
        jobs=[tagged_job],
        jobs_tags=ListedJob.tags_by_type(),
        jobs_region_tags=[],
        jobs_discord=[],
    )
    soup = BeautifulSoup(html, "html.parser")
    for tag in tagged_job.tech_tags:
        selector = f'[data-jobs-tag="{tag}"][data-jobs-tag-type="technology"]'
        assert (
            soup.select_one(f".jobs-filters {selector}").get_text(strip=True)
            == f"#{tag}"
        )
        assert (
            soup.select_one(f".jobs-item {selector}").get_text(strip=True) == f"#{tag}"
        )


@pytest.mark.asyncio
async def test_discord_generalizes_forum_tags_but_keeps_detailed_hashtags(tagged_job):
    ai = ForumTag(name="AI")
    ai.id = 1551504433190543360
    python = ForumTag(name="Python")
    tags = get_forum_tags(TAGS_MAPPING, [ai, python], tagged_job.tech_tags)

    assert [tag.id for tag in tags] == [1551504433190543360, python.id]
    tagged_job.company_logo_path = None
    params = await prepare_thread_params(tagged_job)
    for tag in tagged_job.tech_tags:
        assert f"`#{tag}`" in params["content"]
