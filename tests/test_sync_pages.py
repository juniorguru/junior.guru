from textwrap import dedent

import pytest

from juniorguru.sync.pages import parse_meta, parse_notes


def test_parse_meta():
    assert (
        parse_meta(
            dedent(
                """
                    ---
                    title: Jak na Git a GitHub
                    description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
                    template: main_handbook.html
                    ---

                    # Git a GitHub

                """
            )
        )
        == dict(
            title="Jak na Git a GitHub",
            description="Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?",
            template="main_handbook.html",
        )
    )


def test_parse_notes():
    assert (
        parse_notes(
            dedent(
                """
                    ---
                    title: Jak na Git a GitHub
                    description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
                    template: main_handbook.html
                    ---

                    # Git a GitHub

                    <!-- {#

                    https://dariagrudzien.com/posts/the-one-about-your-github-account/
                    https://dev.to/yuridevat/how-to-create-a-stunning-github-profile-2mh5

                    {% call blockquote_avatar(
                    'GitHub vyčistit, _polishnout_, upravit. Stejně jako CVčko je to věc, která vás má prodat. Projekty, kterými se chlubit nechceš, radši skryj.',
                    'jiri-psotka.jpg',
                    'Jiří Psotka'
                    ) %}
                    Jiří Psotka, recruiter v [Red Hatu](https://red.ht/juniorguru) v prvním dílu podcastu junior.guru
                    {% endcall %}

                    #} -->
                """
            )
        )
        == dedent(
            """
                https://dariagrudzien.com/posts/the-one-about-your-github-account/
                https://dev.to/yuridevat/how-to-create-a-stunning-github-profile-2mh5

                {% call blockquote_avatar(
                'GitHub vyčistit, _polishnout_, upravit. Stejně jako CVčko je to věc, která vás má prodat. Projekty, kterými se chlubit nechceš, radši skryj.',
                'jiri-psotka.jpg',
                'Jiří Psotka'
                ) %}
                Jiří Psotka, recruiter v [Red Hatu](https://red.ht/juniorguru) v prvním dílu podcastu junior.guru
                {% endcall %}
            """
        ).strip()
    )


def test_parse_notes_multiple():
    with pytest.raises(ValueError):
        parse_notes(
            dedent(
                """
                    <!-- {#
                    https://dariagrudzien.com/posts/the-one-about-your-github-account/
                    #} -->

                    <!-- {#
                    https://dev.to/yuridevat/how-to-create-a-stunning-github-profile-2mh5
                    #} -->
                """
            )
        )


def test_parse_notes_none():
    assert parse_notes("hello world") is None


def test_parse_notes_empty():
    assert (
        parse_notes(
            """
                <!-- {#

                #} -->
            """
        )
        is None
    )
