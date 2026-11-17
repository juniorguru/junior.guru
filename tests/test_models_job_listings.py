from jg.coop.models.job import (
    REGION_LISTINGS,
    ListedJob,
    RegionListing,
    get_region_listings,
)


def test_get_region_listings():
    assert get_region_listings(["Hradec Králové"]) == [
        RegionListing(slug="remote", tag_slug="remote", name="Na dálku"),
        RegionListing(
            slug="hradec-kralove", tag_slug="hradeckralove", name="Hradec Králové"
        ),
    ]


def test_region_listing_doc_path():
    region_listing = RegionListing(
        slug="hradec-kralove", tag_slug="hradeckralove", name="Hradec Králové"
    )

    assert region_listing.doc_path == "jobs/hradec-kralove.jinja"


def test_region_tags_match_region_listings():
    tag_slugs = [tag.slug for tag in ListedJob.region_tags()]

    assert tag_slugs == [region_listing.tag_slug for region_listing in REGION_LISTINGS]
