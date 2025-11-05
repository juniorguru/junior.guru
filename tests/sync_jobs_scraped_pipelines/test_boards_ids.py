import pytest

from jg.coop.sync.jobs_scraped.pipelines.boards_ids import process


@pytest.mark.parametrize(
    "item, expected",
    [
        (
            dict(
                url="https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/"
            ),
            ["juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57"],
        ),
        (
            dict(
                url="https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate"
            ),
            ["startupjobs#48407"],
        ),
        (
            dict(
                url="https://remoteok.io/remote-jobs/remote-freelance-writer-doughnut-195318"
            ),
            ["remoteok#195318"],
        ),
        (
            dict(
                url="https://remoteok.com/remote-jobs/remote-freelance-writer-doughnut-195318"
            ),
            ["remoteok#195318"],
        ),
        (
            dict(
                url="https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz"
            ),
            ["linkedin#3471051593"],
        ),
        (
            dict(
                url="https://7.jobs.cz/detail-pozice?r=detail&id=1616053421&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c"
            ),
            ["jobscz#1616053421"],
        ),
        (
            dict(
                url="https://kdejinde.jobs.cz/detail-pozice?r=detail&id=1587451732&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c#fms"
            ),
            ["jobscz#1587451732"],
        ),
        (
            dict(
                url="https://beta.www.jobs.cz/rpd/1615996654/?searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=233"
            ),
            ["jobscz#1615996654"],
        ),
        (
            dict(
                url="https://beta.www.jobs.cz/fp/fortuna-game-a-s-5118444/1614397443/?positionOfAdInAgentEmail=0&searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=317"
            ),
            ["jobscz#1614397443"],
        ),
        (
            dict(
                url="https://cz.linkedin.com/jobs/view/produk%C4%8Dn%C3%AD-food-redaktorka-at-medi%C3%A1ln%C3%AD-skupina-mafra-4334201503?refId=kJU16eXE%2FMi6hQo%2Fw3EdaQ%3D%3D&trackingId=JW1qDjdfJGsjYA2es4DzKA%3D%3D&position=24&pageNum=0"
            ),
            ["linkedin#4334201503"],
        ),
        (
            dict(
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0"
                ],
                url="https://www.linkedin.com/jobs/view/4334211481",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
            ),
            ["linkedin#4334211481", "jobscz#2000805294"],
        ),
    ],
)
@pytest.mark.asyncio
async def test_boards_ids(item, expected):
    item = await process(item)

    assert item["boards_ids"] == sorted(expected)
