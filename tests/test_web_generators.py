from jg.coop.models.job import TagType
from jg.coop.models.jobs_listing import JobsListing
from jg.coop.web.generators import build_listing_meta, generate_jobs_listing_pages


LISTING = JobsListing(
    slug="brno",
    type=TagType.LOCATION,
    tag_slugs=["brno"],
    name="Brno",
    heading="Práce pro juniory: Brno",
    title="Práce v IT, Brno",
    description="Jaké nabízí Brno příležitosti?",
)


def test_jobs_listing_pages_have_unique_paths():
    paths = [document.path for document in generate_jobs_listing_pages()]

    assert len(paths) == len(set(paths))


def test_jobs_listing_pages_paths():
    paths = {document.path for document in generate_jobs_listing_pages()}

    assert {
        "jobs/remote.jinja",
        "jobs/hradec-kralove.jinja",
        "jobs/python.jinja",
        "jobs/part-time.jinja",
    } <= paths


def test_build_listing_meta():
    base_meta = {"title": "Jobs", "description": "All jobs", "template": "x.html"}

    assert build_listing_meta(base_meta, LISTING) == {
        "title": "Práce v IT, Brno",
        "description": "Jaké nabízí Brno příležitosti?",
        "template": "x.html",
        "jobs_listing_slug": "brno",
    }
