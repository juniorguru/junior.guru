from jg.coop.models.jobs_listing import JobsListingPage
from jg.coop.web.generators import build_listing_meta, build_student_pass_meta


def test_build_listing_meta():
    base_meta = {"title": "Jobs", "description": "All jobs", "template": "x.html"}
    listing = JobsListingPage(
        slug="brno", title="Práce v IT, Brno", description="Jaké nabízí Brno?"
    )

    assert build_listing_meta(base_meta, listing) == {
        "title": "Práce v IT, Brno",
        "description": "Jaké nabízí Brno?",
        "template": "x.html",
        "jobs_listing_slug": "brno",
    }


def test_build_student_pass_meta_is_noindex():
    assert build_student_pass_meta("Czechitas", "czechitas")["noindex"] is True
