from markdown import markdown

from jg.coop.lib.md_toc import TocExtension


def render(markdown_text: str) -> str:
    return markdown(markdown_text, extensions=[TocExtension(permalink="#")])


def test_h1_has_no_permalink():
    assert render("# Title") == '<h1 id="title">Title</h1>'


def test_h2_has_permalink():
    assert render("## Section") == (
        '<h2 id="section">Section'
        '<a class="headerlink" href="#section" title="Permanent link">#</a>'
        "</h2>"
    )


def test_registers_as_toc():
    """Replaces the built-in toc processor, which MkDocs always loads"""
    html = markdown(
        "# Title",
        extensions=["toc", TocExtension(permalink="#")],
    )

    assert html == '<h1 id="title">Title</h1>'
