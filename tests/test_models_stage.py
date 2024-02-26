import random
import uuid
from typing import Generator

import pytest

from juniorguru.models.base import SqliteDatabase
from juniorguru.models.page import Page
from juniorguru.models.stage import Stage

from testing_utils import prepare_test_db


@pytest.fixture
def test_db() -> Generator[SqliteDatabase, None, None]:
    yield from prepare_test_db([Stage, Page])


def create_stage(**kwargs) -> Stage:
    unique_id = uuid.uuid4().hex
    return Stage.create(
        position=kwargs.get("position", random.randint(1, 100)),
        slug=kwargs.get("slug", f"learning-{unique_id}"),
        title=kwargs.get("title", f"Učím se #{unique_id}"),
        icon=kwargs.get("icon", f"scooter-{unique_id}"),
        description=kwargs.get("description", "Bla bla bla."),
    )


def test_listing_sorts_by_position(test_db: SqliteDatabase):
    stage3 = create_stage(position=3)
    stage1 = create_stage(position=1)
    stage2 = create_stage(position=2)

    assert list(Stage.listing()) == [stage1, stage2, stage3]


def test_list_pages(test_db: SqliteDatabase):
    stage = create_stage(slug="learning")
    Page.create(
        src_uri="handbook/remote.md",
        dest_uri="handbook/remote/index.html",
        title="Foo",
        nav_name="Foo",
        stages=["foo"],
    )
    page2 = Page.create(
        src_uri="handbook/university.md",
        dest_uri="handbook/university/index.html",
        title="Bar",
        nav_name="Bar",
        stages=["bar", "learning"],
    )
    page3 = Page.create(
        src_uri="handbook/women.md",
        dest_uri="handbook/women/index.html",
        title="Moo",
        nav_name="Moo",
        stages=["learning"],
    )

    assert list(stage.list_pages) == [page2, page3]


def test_list_pages_skips_noindex(test_db: SqliteDatabase):
    stage = create_stage(slug="learning")
    Page.create(
        src_uri="handbook/university.md",
        dest_uri="handbook/university/index.html",
        title="Foo",
        nav_name="Foo",
        stages=["bar", "learning"],
        noindex=True,
    )
    page2 = Page.create(
        src_uri="handbook/women.md",
        dest_uri="handbook/women/index.html",
        title="Moo",
        nav_name="Moo",
        stages=["learning"],
        noindex=False,
    )

    assert list(stage.list_pages) == [page2]


def test_list_pages_skips_without_nav_name(test_db: SqliteDatabase):
    stage = create_stage(slug="learning")
    Page.create(
        src_uri="handbook/university.md",
        dest_uri="handbook/university/index.html",
        title="Foo",
        nav_name=None,
        stages=["bar", "learning"],
    )
    page2 = Page.create(
        src_uri="handbook/women.md",
        dest_uri="handbook/women/index.html",
        title="Moo",
        nav_name="Moo",
        stages=["learning"],
    )

    assert list(stage.list_pages) == [page2]
