import sys
from pathlib import Path

from lxml import html


root_el = html.fromstring(Path(sys.argv[1]).read_text())

for el in root_el.cssselect('[id]'):
    if el.tag == 'nav':
        continue
    elif el.tag == 'section':
        h2_el = el.cssselect('h2')[0]
        print(f"## {h2_el.text_content().strip()}    <span id=\"{el.get('id')}\"></span>")
    elif el.tag == 'h2':
        print(f"## {el.text_content().strip()}    <span id=\"{el.get('id')}\"></span>")
    elif el.tag == 'h3':
        print(f"### {el.text_content().strip()}    <span id=\"{el.get('id')}\"></span>")
    else:
        print(f'Unexpected element: {el}')
