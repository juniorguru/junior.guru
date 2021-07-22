from juniorguru.lib.md import md, strip_links


def test_md():
    markup = md('call me **maybe**  \ncall me Honza')
    assert str(markup) == '<p>call me <strong>maybe</strong><br>\ncall me Honza</p>'


def test_md_headings():
    markup = md((
        '# heading1\n'
        '## heading2\n'
        '### heading3\n'
    ))
    assert str(markup) == (
        '<h1 id="heading1">heading1</h1>\n'
        '<h2 id="heading2">heading2</h2>\n'
        '<h3 id="heading3">heading3</h3>'
    )


def test_strip_links():
    assert strip_links('''
        Sedm let na ČRo Wave moderoval své [Dubové okénko
        Prince Wilibalda](https://hledani.rozhlas.cz/iRadio/?query=Dubov%C3%A9+ok%C3%A9nko+Prince+Wilibalda&reader=&stanice%5B%5D=%C4%8CRo+Radio+Wave&porad%5B%5D=Sc%C3%A9na+s+Jakubem+Joh%C3%A1nkem).
    ''') == '''
        Sedm let na ČRo Wave moderoval své Dubové okénko
        Prince Wilibalda.
    '''
