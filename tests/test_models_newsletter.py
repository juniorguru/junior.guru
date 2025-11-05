from textwrap import dedent

from jg.coop.models.newsletter import process_content_html


def test_process_content_html_removes_double_br():
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

    assert process_content_html(body) == expected


def test_process_content_html_preserves_chart():
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
    assert process_content_html(chart) == chart


def test_process_content_html_strips_emoji_from_h2():
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

    assert process_content_html(body) == expected
