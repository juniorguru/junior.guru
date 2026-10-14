from textwrap import dedent

from jg.coop.models.newsletter import (
    content_to_html,
    edit_content_html,
    get_headings,
    get_issue_description,
)


def test_content_to_html_with_markdown():
    body = dedent(
        """
            # Nadpis

            Toto je **tučný** text s [odkazem](https://example.com).

            - Položka 1
            - Položka 2
        """
    ).strip()
    expected = dedent(
        """
            <h1 id="nadpis">Nadpis</h1>
            <p>Toto je <strong>tučný</strong> text s <a href="https://example.com">odkazem</a>.</p>
            <ul>
            <li>Položka 1</li>
            <li>Položka 2</li>
            </ul>
        """
    ).strip()

    assert content_to_html(body) == expected


def test_content_to_html_with_html():
    body = dedent(
        """
            <h1>Nadpis</h1>
            <p>Toto je <strong>tučný</strong> text s <a href="https://example.com">odkazem</a>.</p>
            <ul>
            <li>Položka 1</li>
            <li>Položka 2</li>
            </ul>
        """
    ).strip()

    assert content_to_html(body) == body


def test_edit_content_html_removes_double_br():
    body = dedent(
        """
            <p>
            <strong>12.11. Brno</strong>, komunita kolem frontendu:<br>
            <br>
            <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.meetup.com/frontendisti/events/311580722/">Brno: Přístupný diskuzní večer</a>
            </p>
        """
    ).strip()
    expected = dedent(
        """
            <p>
            <strong>12.11. Brno</strong>, komunita kolem frontendu:<br>
            <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.meetup.com/frontendisti/events/311580722/">Brno: Přístupný diskuzní večer</a>
            </p>
        """
    ).strip()

    assert edit_content_html(body) == expected


def test_edit_content_html_preserves_chart():
    chart = dedent(
        """
            <p>
            🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨 81× #testing<br>
            🟨🟨🟨🟨🟨🟨🟨🟨🟨 78× #database<br>
            🟨🟨🟨🟨🟨🟨🟨 61× #javascript<br>
            🟨🟨🟨🟨🟨🟨 56× #python<br>
            🟨🟨🟨🟨🟨 46× #css<br>
            🟨🟨🟨🟨🟨 44× #html<br>
            🟨🟨🟨🟨🟨 41× #excel<br>
            🟨🟨🟨 31× #csharp<br>
            🟨🟨🟨 29× #git<br>
            🟨🟨 24× #linux<br>
            </p>
        """
    ).strip()
    assert edit_content_html(chart) == chart


def test_edit_content_html_strips_emoji_from_h2():
    body = dedent(
        """
            <h2>🚀 Nové kurzy a články</h2>
            <h2>🔥 Akce a meetupy</h2>
        """
    ).strip()
    expected = dedent(
        """
            <h2>Nové kurzy a články</h2>
            <h2>Akce a meetupy</h2>
        """
    ).strip()

    assert edit_content_html(body) == expected


def test_edit_content_html_adds_trailing_slash_to_course_urls():
    body = (
        '<a href="https://junior.guru/courses/engeto">Engeto</a> '
        '<a href="https://junior.guru/courses/42prague?utm_source=x">42</a> '
        '<a href="https://junior.guru/courses/czechitas/">Czechitas</a> '
        '<a href="https://junior.guru/courses/">Kurzy</a>'
    )
    expected = (
        '<a href="https://junior.guru/courses/engeto/">Engeto</a> '
        '<a href="https://junior.guru/courses/42prague/?utm_source=x">42</a> '
        '<a href="https://junior.guru/courses/czechitas/">Czechitas</a> '
        '<a href="https://junior.guru/courses/">Kurzy</a>'
    )

    assert edit_content_html(body) == expected


def test_get_headings():
    content_html = dedent(
        """
            <h1>Nadpis</h1>
            <h2 id="trh">Čísla z <strong>trhu</strong></h2>
            <p>Text</p>
            <h3>AI a junioři</h3>
            <h4>Detail</h4>
        """
    )

    assert get_headings(content_html) == ["Čísla z trhu", "AI a junioři"]


def test_get_issue_description():
    description = get_issue_description(
        "Září 2026 ve světě IT juniorů",
        ["Čísla z trhu", "AI a junioři", "Podcast", "Vyjednávání mzdy"],
        recurring_headings={"Čísla z trhu", "Podcast"},
    )

    assert description == (
        "Září 2026 ve světě IT juniorů. Témata: AI a junioři, Vyjednávání mzdy"
    )


def test_get_issue_description_only_recurring_headings():
    description = get_issue_description(
        "Říjen 2025 ve světě IT juniorů",
        ["Čísla z trhu", "Podcast"],
        recurring_headings={"Čísla z trhu", "Podcast"},
    )

    assert description == (
        "Říjen 2025 ve světě IT juniorů. Témata: Čísla z trhu, Podcast"
    )


def test_get_issue_description_shortened():
    description = get_issue_description(
        "Září 2026 ve světě IT juniorů",
        [f"Velmi dlouhé téma číslo {i}" for i in range(10)],
        recurring_headings=set(),
    )

    assert len(description) <= 160
