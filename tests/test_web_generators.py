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


def test_build_student_pass_meta():
    assert build_student_pass_meta("Czechitas", "czechitas") == {
        "title": "Propustka do\u00a0klubu pro studenty Czechitas",
        "description": (
            "Studenti Czechitas mají v\u00a0klubu junior.guru "
            "kromě dvou týdnů na\u00a0vyzkoušení ještě měsíc zdarma."
        ),
        "course_provider_slug": "czechitas",
        "noindex": True,
    }
