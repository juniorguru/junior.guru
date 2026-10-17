from itertools import chain

from jg.coop.web.generators import (
    generate_employment_type_jobs_pages,
    generate_region_jobs_pages,
    generate_tech_jobs_pages,
)


def test_jobs_listing_pages_have_unique_paths():
    paths = [
        document.path
        for document in chain(
            generate_region_jobs_pages(),
            generate_employment_type_jobs_pages(),
            generate_tech_jobs_pages(),
        )
    ]

    assert len(paths) == len(set(paths))
