from collections import namedtuple
from datetime import UTC, date, datetime

import pytest
from mkdocs.structure.files import File

from jg.coop.lib import template_filters


def test_email_link():
    markup = str(template_filters.email_link("xyz@example.com"))
    assert (
        markup == '<a href="mailto:xyz&#64;example.com">xyz&#64;<!---->example.com</a>'
    )


def test_remove_p():
    markup = str(
        template_filters.remove_p(
            '<p>call me <b>maybe</b></p>  \n<p class="hello">call me Honza</p>'
        )
    )
    assert markup == "call me <b>maybe</b>  \ncall me Honza"


@pytest.mark.parametrize(
    "dt, expected",
    [
        (datetime(2020, 4, 21, 12, 1, 48), "14:01"),
        (datetime(2020, 4, 21, 20, 30, 00, tzinfo=UTC), "22:30"),
        (datetime(2020, 4, 21, 5, 0, 48), "7:00"),
    ],
)
def test_local_time(dt, expected):
    assert template_filters.local_time(dt) == expected


@pytest.mark.parametrize(
    "dt, expected",
    [
        (datetime(2020, 4, 21, 12, 1, 48), "úterý"),
        (date(2020, 4, 21), "úterý"),
    ],
)
def test_weekday(dt, expected):
    assert template_filters.weekday(dt) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(134, "134", id="hundreds"),
        pytest.param(2179, "2.179", id="thousands"),
        pytest.param(21790, "21.790", id="tens thousands"),
    ],
)
def test_thousands(value, expected):
    assert template_filters.thousands(value) == expected


@pytest.mark.parametrize(
    "items,n,expected",
    [
        pytest.param(
            ["x"],
            4,
            {"x"},
            id="len(items) < n",
        ),
        pytest.param(
            ["x", "y"],
            2,
            {"x", "y"},
            id="len(items) == n",
        ),
    ],
)
def test_sample(items, n, expected):
    assert set(template_filters.sample(items, n)) == expected


def test_sample_random():
    random_called = False

    def random_sample(items, n):
        nonlocal random_called
        random_called = True
        return items[:n]

    assert set(
        template_filters.sample(["x", "y", "z"], 2, sample_fn=random_sample)
    ) == {"x", "y"}
    assert random_called is True


StubJob = namedtuple("Job", ["id", "is_submitted"])


@pytest.mark.parametrize(
    "jobs,n,expected",
    [
        pytest.param(
            [StubJob(id=1, is_submitted=False), StubJob(id=2, is_submitted=False)],
            4,
            {StubJob(id=1, is_submitted=False), StubJob(id=2, is_submitted=False)},
            id="len(jobs) < n",
        ),
        pytest.param(
            [StubJob(id=1, is_submitted=False), StubJob(id=2, is_submitted=False)],
            2,
            {StubJob(id=1, is_submitted=False), StubJob(id=2, is_submitted=False)},
            id="len(jobs) == n",
        ),
        pytest.param(
            [
                StubJob(id=1, is_submitted=False),
                StubJob(id=2, is_submitted=True),
                StubJob(id=3, is_submitted=True),
            ],
            2,
            {StubJob(id=2, is_submitted=True), StubJob(id=3, is_submitted=True)},
            id="preferred jobs have priority",
        ),
    ],
)
def test_sample_jobs(jobs, n, expected):
    assert set(template_filters.sample_jobs(jobs, n)) == expected


def test_sample_jobs_not_enough_preferred_jobs():
    random_called = False

    def random_sample(jobs, n):
        nonlocal random_called
        random_called = True
        return jobs[:n]

    assert set(
        template_filters.sample_jobs(
            [
                StubJob(id=1, is_submitted=False),
                StubJob(id=2, is_submitted=True),
                StubJob(id=3, is_submitted=False),
            ],
            2,
            sample_fn=random_sample,
        )
    ) == {
        StubJob(id=1, is_submitted=False),
        StubJob(id=2, is_submitted=True),
    }
    assert random_called is True


def test_icon():
    markup = template_filters.icon("check-square")

    assert str(markup) == '<i class="bi bi-check-square"></i>'


def test_icon_with_alt():
    markup = template_filters.icon("check-square", alt="Alt Text")

    assert (
        str(markup)
        == '<i class="bi bi-check-square" role="img" aria-label="Alt Text"></i>'
    )


def test_icon_with_classes():
    markup = template_filters.icon("check-square", "text-success bi")

    assert str(markup) == '<i class="bi bi-check-square text-success"></i>'


def test_docs_url():
    assert (
        template_filters.docs_url(
            [
                File("privacy.md", "jg/coop/web/docs", "public", True),
                File("club.md", "jg/coop/web/docs", "public", True),
                File("topics/csharp.md", "jg/coop/web/docs", "public", True),
            ],
            "club.md",
        )
        == "club/"
    )


def test_revenue_categories():
    assert template_filters.revenue_categories(
        {
            "donations": 10,
            "jobs": 20,
            "memberships": 1,
            "sponsorships": 4,
        }
    ) == [
        ("inzerce nabídek práce", 20),
        ("dobrovolné příspěvky", 10),
        ("příspěvky sponzorů", 4),
        ("členství v klubu", 1),
    ]


def test_revenue_categories_less():
    assert template_filters.revenue_categories(
        {
            "sponsorships": 4,
            "jobs": 20,
        }
    ) == [
        ("inzerce nabídek práce", 20),
        ("příspěvky sponzorů", 4),
    ]


def test_revenue_categories_unknown():
    with pytest.raises(KeyError):
        template_filters.revenue_categories(
            {
                "! doesnt exist !": 20,
                "sponsorships": 4,
            }
        )


def test_money_breakdown_ptc():
    assert template_filters.money_breakdown_ptc(
        {
            "discord": 300,
            "lawyer": 500,
            "tax": 100,
        }
    ) == {
        "discord": 34,
        "lawyer": 56,
        "tax": 12,
    }


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://honzajavorek.cz", "static/screenshots/honzajavorek-cz.webp"),
        (
            "https://www.youtube.com/watch?v=123",
            "static/screenshots/youtube-com-watch-v-123.webp",
        ),
        (
            "https://cs.wikipedia.org/wiki/Ildik%C3%B3_(jm%C3%A9no)",
            "static/screenshots/cs-wikipedia-org-wiki-ildiko-jmeno.webp",
        ),
        (
            "https://coreskill.tech/?utm_source=junior.guru&utm_medium=web&utm_campaign=catalog",
            "static/screenshots/coreskill-tech.webp",
        ),
    ],
)
def test_screenshot_url(url, expected):
    assert template_filters.screenshot_url(url) == expected


@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "http://honzajavorek.cz",
            "honzajavorek.cz",
        ),
        (
            "https://www.youtube.com/watch?v=123",
            "youtube.com/watch?v=123",
        ),
        (
            "https://cs.wikipedia.org/wiki/Ildik%C3%B3_(jm%C3%A9no)",
            "cs.wikipedia.org/wiki/Ildikó_(jméno)",
        ),
        (
            "https://coreskill.tech/?utm_source=junior.guru&utm_medium=web&utm_campaign=catalog",
            "coreskill.tech",
        ),
    ],
)
def test_nice_url(url: str, expected: str):
    assert template_filters.nice_url(url) == expected
