import pytest

from jg.coop.lib.job_urls import (
    get_all_urls,
    get_order,
    id_to_url,
    url_to_id,
    urls_to_ids,
)


@pytest.mark.parametrize(
    "id, expected",
    [
        (
            "juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57",
            "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
        ),
        (
            "startupjobs#48407/venture-capital-analyst-associate",
            "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        ),
        (
            "linkedin#3471051593",
            "https://www.linkedin.com/jobs/view/3471051593/",
        ),
        (
            "jobscz#1616053421",
            "https://www.jobs.cz/rpd/1616053421/",
        ),
        (
            "govcz#30093955",
            "https://portal.isoss.gov.cz/irj/portal/anonymous/eosmlistpublic#/detail/30093955",
        ),
    ],
)
def test_id_to_url(id: str, expected: str):
    assert id_to_url(id) == expected


def test_id_to_url_raises_not_implemented_error_for_unknown_name():
    with pytest.raises(NotImplementedError):
        id_to_url("unknownjobboard#123456")


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://example.com",
            None,
        ),
        (
            "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
            "juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57",
        ),
        (
            "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
            "startupjobs#48407/venture-capital-analyst-associate",
        ),
        (
            "https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz",
            "linkedin#3471051593",
        ),
        (
            "https://7.jobs.cz/detail-pozice?r=detail&id=1616053421&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c",
            "jobscz#1616053421",
        ),
        (
            "https://kdejinde.jobs.cz/detail-pozice?r=detail&id=1587451732&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c#fms",
            "jobscz#1587451732",
        ),
        (
            "https://beta.www.jobs.cz/rpd/1615996654/?searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=233",
            "jobscz#1615996654",
        ),
        (
            "https://beta.www.jobs.cz/fp/fortuna-game-a-s-5118444/1614397443/?positionOfAdInAgentEmail=0&searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=317",
            "jobscz#1614397443",
        ),
        (
            "https://www.jobs.cz/rpd/1614397443/",
            "jobscz#1614397443",
        ),
        (
            "https://www.jobs.cz/fp/seznam-cz-a-s-229258/2000657397/?searchId=723dc2df-7db5-4628-9e8b-8e8862da84cb&rps=233",
            "jobscz#2000657397",
        ),
        (
            "https://cz.linkedin.com/jobs/view/produk%C4%8Dn%C3%AD-food-redaktorka-at-medi%C3%A1ln%C3%AD-skupina-mafra-4334201503?refId=kJU16eXE%2FMi6hQo%2Fw3EdaQ%3D%3D&trackingId=JW1qDjdfJGsjYA2es4DzKA%3D%3D&position=24&pageNum=0",
            "linkedin#4334201503",
        ),
        (
            "https://portal.isoss.gov.cz/irj/portal/anonymous/eosmlistpublic#/detail/30093955",
            "govcz#30093955",
        ),
        (
            "https://www.startupjobs.cz/nabidka/97145/backend-engineer?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru",
            "startupjobs#97145/backend-engineer",
        ),
    ],
)
def test_url_to_id(url: str, expected: str):
    assert url_to_id(url) == expected


def test_urls_to_ids_respects_ordering():
    urls = [
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz",
        "https://7.jobs.cz/detail-pozice?r=detail&id=1616053421&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c",
        "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
    ]
    ordering = ["startupjobs", "linkedin", "juniorguru", "jobscz"]
    expected_ids = [
        "startupjobs#48407/venture-capital-analyst-associate",
        "linkedin#3471051593",
        "juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57",
        "jobscz#1616053421",
    ]
    assert urls_to_ids(urls, ordering) == expected_ids


def test_urls_to_ids_deduplicates():
    urls = [
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
    ]
    ordering = ["startupjobs", "linkedin", "juniorguru"]
    expected_ids = [
        "startupjobs#48407/venture-capital-analyst-associate",
        "linkedin#3471051593",
        "juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57",
    ]
    assert urls_to_ids(urls, ordering) == expected_ids


def test_urls_to_ids_skips_unknown_urls():
    urls = [
        "https://example.com",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz",
        "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
    ]
    ordering = ["startupjobs", "linkedin", "juniorguru"]
    expected_ids = [
        "startupjobs#48407/venture-capital-analyst-associate",
        "linkedin#3471051593",
        "juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57",
    ]
    assert urls_to_ids(urls, ordering) == expected_ids


def test_get_order():
    ordering = ["juniorguru", "linkedin", "jobscz"]

    assert get_order("juniorguru#abcdef", ordering) == 0
    assert get_order("linkedin#123456", ordering) == 1
    assert get_order("jobscz#654321", ordering) == 2


def test_get_all_urls():
    item = {
        "url": "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "apply_url": "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate/apply",
        "source_urls": [
            "https://example.com/some-job-posting",
            "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        ],
    }

    assert get_all_urls(item) == [
        "https://example.com/some-job-posting",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate/apply",
    ]


def test_get_all_urls_no_urls():
    assert get_all_urls({}) == []


def test_get_all_urls_empty_apply_url():
    item = {
        "url": "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
    }

    assert get_all_urls(item) == [
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
    ]


def test_get_all_urls_empty_source_urls():
    item = {
        "url": "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "apply_url": "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate/apply",
    }

    assert get_all_urls(item) == [
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate/apply",
    ]
