from jg.coop.models.job import RegionListing, get_region_listings


def test_get_region_listings():
    assert get_region_listings(["Hradec Králové"]) == [
        RegionListing(slug="remote", tag_slug="remote", name="Na dálku"),
        RegionListing(
            slug="hradec-kralove", tag_slug="hradeckralove", name="Hradec Králové"
        ),
    ]
