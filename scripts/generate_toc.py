"""
To generate HTML for the ToC. Usage::

    $ poetry run python scripts/generate_toc.py juniorguru/web/templates/learn.html | pbcopy
"""

import sys
from pathlib import Path
from textwrap import indent

from lxml import html


def main(path):
    ids = []

    output = '<ol class="toc__items">\n'
    html_tree = html.fromstring(Path(path).read_text())
    for h2 in html_tree.cssselect('.content__section-heading'):
        section = [element for element in h2.iterancestors()
                if element.tag == 'section'][0]
        h2_id = section.get('id')
        h2_text = h2.text_content()
        if not h2_id:
            raise Exception(f"Section '{h2_text}' doesn't have ID")
        output += f'  <li class="toc__item"><a class="toc__link" href="#{h2_id}">{h2_text}</a>'
        ids.append(h2_id)

        h3s = section.cssselect('.content__subsection-heading')
        if h3s:
            output += '\n    <ol class="toc__subitems">\n'
            for h3 in h3s:
                h3_id = h3.get('id')
                h3_text = h3.text_content()
                if not h3_id:
                    raise Exception(f"Section '{h3_text}' doesn't have ID")
                output += f'      <li class="toc__subitem"><a class="toc__sublink" href="#{h3_id}">{h3_text}</a></li>\n'
                ids.append(h3_id)
            output += '    </ol>\n  </li>\n'
        else:
            output += '</li>\n'
    output += '</ol>'

    if len(ids) != len(set(ids)):
        raise Exception('There are duplicate IDs!')

    return indent(output, '    ')


if __name__ == '__main__':
    print(main(sys.argv[1]), end='')
