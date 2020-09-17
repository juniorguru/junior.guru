from juniorguru.lib.md import md


def test_md():
    markup = str(md('call me **maybe**  \ncall me Honza'))
    assert markup == '<p>call me <strong>maybe</strong><br>\ncall me Honza</p>'


def test_md_heading_level_base():
    markup = str(md((
        '# Heading 1\n'
        '## Heading 2\n'
        'Paragraph text\n'
    ), heading_level_base=4))
    assert markup == (
        '<h4 id="heading-1">Heading 1</h4>\n'
        '<h5 id="heading-2">Heading 2</h5>\n'
        '<p>Paragraph text</p>'
    )
