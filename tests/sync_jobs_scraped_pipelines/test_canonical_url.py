import pytest

from jg.coop.sync.jobs_scraped.pipelines.canonical_url import process


@pytest.mark.parametrize(
    "item, expected_ids, expected_url",
    [
        (
            dict(
                url="https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/"
            ),
            ["juniorguru#ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57"],
            "https://junior.guru/jobs/ade40e530211c36a309fa370d270da7650ad18462c03c95b0b38de57/",
        ),
        (
            dict(
                url="https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate"
            ),
            ["startupjobs#48407/venture-capital-analyst-associate"],
            "https://www.startupjobs.cz/nabidka/48407/venture-capital-analyst-associate",
        ),
        (
            dict(
                url="https://www.linkedin.com/jobs/view/program%C3%A1tor-ka-webov%C3%BDch-aplikac%C3%AD-junior-at-numerica-s-r-o-3471051593/?originalSubdomain=cz"
            ),
            ["linkedin#3471051593"],
            "https://www.linkedin.com/jobs/view/3471051593/",
        ),
        (
            dict(
                url="https://7.jobs.cz/detail-pozice?r=detail&id=1616053421&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c"
            ),
            ["jobscz#1616053421"],
            "https://www.jobs.cz/rpd/1616053421/",
        ),
        (
            dict(
                url="https://kdejinde.jobs.cz/detail-pozice?r=detail&id=1587451732&rps=233&impressionId=f128203d-0753-453c-944b-c298bb74ee6c#fms"
            ),
            ["jobscz#1587451732"],
            "https://www.jobs.cz/rpd/1587451732/",
        ),
        (
            dict(
                url="https://beta.www.jobs.cz/rpd/1615996654/?searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=233"
            ),
            ["jobscz#1615996654"],
            "https://www.jobs.cz/rpd/1615996654/",
        ),
        (
            dict(
                url="https://beta.www.jobs.cz/fp/fortuna-game-a-s-5118444/1614397443/?positionOfAdInAgentEmail=0&searchId=f128203d-0753-453c-944b-c298bb74ee6c&rps=317"
            ),
            ["jobscz#1614397443"],
            "https://www.jobs.cz/rpd/1614397443/",
        ),
        (
            dict(
                url="https://cz.linkedin.com/jobs/view/produk%C4%8Dn%C3%AD-food-redaktorka-at-medi%C3%A1ln%C3%AD-skupina-mafra-4334201503?refId=kJU16eXE%2FMi6hQo%2Fw3EdaQ%3D%3D&trackingId=JW1qDjdfJGsjYA2es4DzKA%3D%3D&position=24&pageNum=0"
            ),
            ["linkedin#4334201503"],
            "https://www.linkedin.com/jobs/view/4334201503/",
        ),
        (
            dict(
                source_urls=[
                    "https://www.linkedin.com/jobs/search?keywords=junior%20programator&location=Czechia&geoId=104508036&f_TPR=r86400&position=1&pageNum=0"
                ],
                url="https://www.linkedin.com/jobs/view/4334211481",
                apply_url="https://mafra.jobs.cz/detail-pozice?r=detail&id=2000805294",
            ),
            ["jobscz#2000805294", "linkedin#4334211481"],
            "https://www.jobs.cz/rpd/2000805294/",
        ),
        (
            dict(
                url="https://portal.isoss.gov.cz/irj/portal/anonymous/eosmlistpublic#/detail/30093955"
            ),
            ["govcz#30093955"],
            "https://portal.isoss.gov.cz/irj/portal/anonymous/eosmlistpublic#/detail/30093955",
        ),
    ],
)
@pytest.mark.asyncio
async def test_canonical_url(item: dict, expected_ids: list[str], expected_url: str):
    item = await process(item)

    assert item["canonical_ids"] == expected_ids
    assert item["url"] == expected_url


# [
#         ("", None),
#         (None, None),
#         (
#             "https://beta.www.jobs.cz/rpd/1613133866/?searchId=ac8f8a52-70fe-4be5-b32e-9f6e6b1c2b23&rps=228",
#             "https://beta.www.jobs.cz/rpd/1613133866/",
#         ),
#         (
#             "https://beta.www.jobs.cz/fp/alza-cz-a-s-7910630/2000134247/?searchId=868cde40-9065-4e83-83ce-2fe2fa38d529&rps=233",
#             "https://beta.www.jobs.cz/fp/alza-cz-a-s-7910630/2000134247/",
#         ),
#         (
#             "https://skoda-auto.jobs.cz/detail-pozice?r=detail&id=1632413478&rps=233&impressionId=24d42f33-4e37-4a12-98a8-892a30257708",
#             "https://skoda-auto.jobs.cz/detail-pozice?r=detail&id=1632413478",
#         ),
#         (
#             "https://mafra.jobs.cz/detail-pozice?r=detail&id=2000811755&impressionId=b81a20bd-36ec-4219-9a49-4f8def3b9a23",
#             "https://mafra.jobs.cz/detail-pozice?r=detail&id=2000811755",
#         ),
#         (
#             "https://www.profesia.sk/praca/engie-services-slovensko/O5122216?search_id=6acdb21d-5ab0-40b3-9c63-dca56adbe1cf",
#             "https://www.profesia.sk/praca/engie-services-slovensko/O5122216",
#         )
#         (
#             "https://www.linkedin.com/jobs/view/4315558510/?alternateChannel=search&eBP=CwEAAAGaWIfYWv5ZSnS_Rnx6GBsYj6OcQ2na8kqmcgsVIheREs19VE65ulfTe4sS_GHyGaGtG-XiC6TzDvjaBIA14U6KFNhiaKrAMI9q0bgdoLI_U90utP_o1kxwEu614bl7kucxm6yaryADlUg190S7SLQOQ-FcJbFPh7l_JhptzRmpmMls1d2FXQ8vYin8VUXAYb1XdExGj295ruzaJEWgqBmWlPaECZTneORpEAPFlnkt52qNZeziUbM0poxqJYhtt4BuwyfhrXD3l14ol0P76-z5e5OoOQkUiLP8qao4XhsiZYykCqU7B7k_HVr0Fl9HMtPRermt2hLgTJczlbbOD_VWX7Qtw9qveJ-stWxRxjKHMjLNod8rmBZDSoEq6afj3UYveJjLv5jgcW1XYLJKjOhpVdvnb1IJVQGfqrJZ-35OyuBYtrIxdse1qWHrE9pKvcsqwJYS8i-UXM2vGcyQb3Yeve7ykc9lT1iqLaX1C6If2c8&refId=4uFL5BL38fGAA08FPsINDQ%3D%3D&trackingId=Cb90knCTCsotUTAAA%2FW9ZA%3D%3D&trk=d_flagship3_search_srp_jobs&lipi=urn%3Ali%3Apage%3Ad_flagship3_search_srp_jobs%3BfA1UrftkQqGddOBOfK1tGQ%3D%3D",
#             "https://www.linkedin.com/jobs/view/4315558510/",
#         ),
#         (
#             "https://www.linkedin.com/jobs/view/4320504036/?alternateChannel=search&eBP=CwEAAAGaWIfYWi87esUUcHh9OslYdV02QKZRJMlfjtPpCn5D7awwtPZGdl2d6jYwqTp0Okt1gDGarEmRru02Yj4JMCoXXPPWGEqmAij2m8QcuJvlZgfxGJ-cbdPd_lzfLwFgj9bjtd2iu9_-3SAfSgb9jbS0bGiMK6bTAUO3aZZSFKq1Af8wJSEF1KFHeLEecD42pKEty-cntXTgao72laXA6Mr_Sy06U9G1uox3q4RYnBJ0o3Na5ZXAxl9So7I8469u33j6aZOmebvlPARyp5rTtJllU6r0eQwmSdxxFPr3-z775kFBhaxsU_H4ZG_WEaZmimaimvV28DcOTP1fi68Ip1p6ZHTz8tgX-CF89hbxKWigG1txVH0Eu03mMHWyzmSXlRzUmS10OT3lWnRxFCHu_K2peu-2QW1-26QEfw3HUC-o8v6A0XXjpdkC4_bjg96KVMzqXTj1W9Y0eiWzFFkcbRG5TerKYwCz57Lh7sEYY1wyj_IIEHRL9vgP60Hi2EkRkLh0v-3g32EBx5vec8Rato--Rw",
#             "https://www.linkedin.com/jobs/view/4320504036/",
#         ),
#         (
#             "https://erecruitment.eib.org/psc/hr/EIBJOBS/CAREERS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&focus=Applicant&SiteId=1&JobOpeningId=110956&PostingSeq=1&aSource=LinkedIn",
#             "https://erecruitment.eib.org/psc/hr/EIBJOBS/CAREERS/c/HRS_HRAM_FL.HRS_CG_SEARCH_FL.GBL?Page=HRS_APP_JBPST_FL&focus=Applicant&SiteId=1&JobOpeningId=110956&PostingSeq=1&aSource=juniorguru"
#         ),
#         (
#             "https://www.startupjobs.cz/nabidka/97145/backend-engineer-for-web-automation-team-node-js?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru",
#             "https://www.startupjobs.cz/nabidka/97145/backend-engineer-for-web-automation-team-node-js?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru",
#         ),
#         (
#             "https://www.startupjobs.cz/nabidka/97145/backend-engineer-for-web-automation-team-node-js?utm_source=linkedin&utm_medium=cpc&utm_campaign=linkedin",
#             "https://www.startupjobs.cz/nabidka/97145/backend-engineer-for-web-automation-team-node-js?utm_source=juniorguru&utm_medium=cpc&utm_campaign=juniorguru",
#         ),
#         (
#             "https://cdc-data-s-r-o.nelisa.com/cs/offer/68821b60-5060-4710-bf82-d53fb50acd62?utm_content=cdc-data-s-r-o_krotime-chaos-v-dokumentech-konzultant-systemu-m-files-komunikace-it-dobre-napady-2-dny-home-office-a-tym-kde-zalezi-na-kazdem-1760010492",
#             "https://cdc-data-s-r-o.nelisa.com/cs/offer/68821b60-5060-4710-bf82-d53fb50acd62?utm_source=juniorguru",
#         ),
#         (
#             "https://ibmglobal.avature.net/en_US/careers/JobDetail?jobId=70246&source=SN_LinkedIn",
#             "https://ibmglobal.avature.net/en_US/careers/JobDetail?jobId=70246&source=SN_juniorguru"
#         ),
#         (
#             "https://solera.wd5.myworkdayjobs.com/Global_Career_Site/job/Prague/Vehicle-data-editor_JR-018650?source=LinkedIn",
#             "https://solera.wd5.myworkdayjobs.com/Global_Career_Site/job/Prague/Vehicle-data-editor_JR-018650?source=juniorguru"
#         ),
#         (
#             "https://jsv3.recruitics.com/redirect?rx_cid=3436&rx_jobId=R-01331068&rx_url=https%3A%2F%2Fjobs.thermofisher.com%2Fglobal%2Fen%2Fjob%2FR-01331068%2FIntern-Manual-Software-System-Tester%3Frx_ch%3Djobpost%26rx_id%3D9dafb86e-a91d-11f0-9efd-1fe13fa3b0bb%26rx_job%3DR-01331068%26rx_medium%3Dpost%26rx_paid%3D0%26rx_r%3Dnone%26rx_source%3Dlinkedin%26rx_ts%3D20251101T204036Z%26rx_vp%3Dlinkedindirectindex%26utm_medium%3Dpost%26utm_source%3Drecruitics_linkedindirectindex&refId=34jd24",
#             "https://jobs.thermofisher.com/global/en/job/R-01331068/Intern-Manual-Software-System-Tester?rx_ch=jobpost&rx_id=9dafb86e-a91d-11f0-9efd-1fe13fa3b0bb&rx_job=R-01331068&rx_medium=post&rx_paid=0&rx_r=none&rx_source=juniorguru&rx_ts=20251101T204036Z&rx_vp=juniorgurudirectindex&utm_medium=post&utm_source=juniorguru"
#         ),
#         (
#             "https://example.com/redirect?url=https%3A%2F%2Fjobs.thermofisher.com%2Fglobal%2Fen%2Fjob%2FR-01331068%2FIntern-Manual-Software-System-Tester%3Frx_ch%3Djobpost%26rx_id%3D9dafb86e-a91d-11f0-9efd-1fe13fa3b0bb%26rx_job%3DR-01331068",
#             "https://jobs.thermofisher.com/global/en/job/R-01331068/Intern-Manual-Software-System-Tester?rx_ch=jobpost&rx_id=9dafb86e-a91d-11f0-9efd-1fe13fa3b0bb&rx_job=R-01331068"
#         ),
#         (
#             "https://molgroup.taleo.net/careersection/external/jobdetail.ftl?job=25002550&lang=en&src=linkedin",
#             "https://molgroup.taleo.net/careersection/external/jobdetail.ftl?job=25002550&lang=en&src=juniorguru"
#         )
#     ],
