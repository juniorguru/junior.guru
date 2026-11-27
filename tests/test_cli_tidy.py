from textwrap import dedent

import pytest

from jg.coop.cli.tidy import (
    get_jinja_calls,
    get_jinja_imports,
    get_unused_jinja_imports,
    remove_unused_jinja_imports,
)


@pytest.mark.parametrize(
    "markup, expected",
    [
        (
            dedent(
                """
                    {% from 'macros.html' import blockquote, blockquote_avatar,
                        blockquote_toxic, lead
                    with context %}
                """
            ),
            {"blockquote", "blockquote_avatar", "blockquote_toxic", "lead"},
        ),
        (
            dedent(
                """
                    {% from 'macros.html' import blockquote, blockquote_avatar without context %}
                """
            ),
            {"blockquote", "blockquote_avatar"},
        ),
        (
            dedent(
                """
                    {% from 'macros.html' import blockquote, blockquote_avatar %}
                """
            ),
            {"blockquote", "blockquote_avatar"},
        ),
    ],
)
def test_get_jinja_imports(markup: str, expected: set[str]):
    assert get_jinja_imports(markup) == expected


@pytest.mark.parametrize(
    "markup",
    [
        dedent(
            """
                {% from 'macros.html' import blockquote, blockquote_avatar %}
                foo boo
                moo
                {% from 'macros.html' import lead, note %}
            """
        ),
        dedent(
            """
                {% from 'macros.html' import blockquote, blockquote_avatar %}
                foo boo
                moo
                {% from 'macros.html' import blockquote, lead, note %}
            """
        ),
    ],
)
def test_get_jinja_imports_raises(markup: str):
    with pytest.raises(ValueError):
        assert get_jinja_imports(markup)


@pytest.mark.parametrize(
    "markup, expected",
    [
        (
            dedent(
                """
                    {{ video_card_engeto(
                        'Nejčastější mýty o práci v IT',
                        '5min',
                        'https://www.youtube.com/watch?v=2Km3orTYFrM&list=PLrsbT5TVJXZa2daxo8_3NagDzPqHjBEpI',
                        'Musím mít talent na techniku nebo matematiku? Záleží na věku? Potřebuji vysokou školu?',
                    ) }}
                """
            ),
            {"video_card_engeto"},
        ),
        (
            dedent(
                """
                    {{ link_card(
                        'Make',
                        'https://www.make.com/',
                        'Největší platforma, podporuje i české služby jako Fakturoid nebo Fio Banka.'
                    ) }}

                    {{ link_card(
                        'Zapier',
                        'https://zapier.com/',
                        'Druhá nejznámější platforma pro automatizaci.'
                    ) }}
                """
            ),
            {"link_card"},
        ),
        (
            dedent(
                """
                    {% call note(standout=True) %}
                        {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
                    {% endcall %}
                """
            ),
            {"note"},
        ),
        (
            dedent(
                """
                    {{ img('static/chick' + loop.index|string + '.svg', 'Kuře', 50, 50, lazy=False) }}

                    {% call note(standout=True) %}
                        {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
                    {% endcall %}
                """
            ),
            {"img", "note"},
        ),
    ],
)
def test_get_jinja_calls(markup: str, expected: set[str]):
    assert get_jinja_calls(markup) == expected


MARKUP_WITH_GLOBAL_CALL = dedent(
    """
        {% from 'macros.html' import img, lead, note with context %}
        {{ graph_json_ld(website_json_ld()) }}
        {% call lead() %}Ahoj{% endcall %}
        {{ img('a.svg', 'A') }}
    """
)


def test_get_unused_jinja_imports():
    assert get_unused_jinja_imports(MARKUP_WITH_GLOBAL_CALL) == {"note"}


def test_remove_unused_jinja_imports_keeps_globals_out():
    markup = remove_unused_jinja_imports(MARKUP_WITH_GLOBAL_CALL)

    assert "{% from 'macros.html' import img, lead with context %}" in markup
