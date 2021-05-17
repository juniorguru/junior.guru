from juniorguru.lib.md import md, strip_links


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


def test_strip_links():
    assert strip_links('''
        Sedm let na ČRo Wave moderoval své [Dubové okénko
        Prince Wilibalda](https://hledani.rozhlas.cz/iRadio/?query=Dubov%C3%A9+ok%C3%A9nko+Prince+Wilibalda&reader=&stanice%5B%5D=%C4%8CRo+Radio+Wave&porad%5B%5D=Sc%C3%A9na+s+Jakubem+Joh%C3%A1nkem).
    ''') == '''
        Sedm let na ČRo Wave moderoval své Dubové okénko
        Prince Wilibalda.
    '''
