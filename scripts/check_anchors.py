# https://github.com/stevenvachon/broken-link-checker/issues/166

import sys
from pathlib import Path

from lxml import html


PUBLIC_DIR = Path(__file__).parent.parent / 'public'


links = []
ids = set()

for path in PUBLIC_DIR.glob('**/*.html'):
    doc_name = f'/{path.relative_to(PUBLIC_DIR)}'
    doc_name = doc_name[:-10] if doc_name.endswith('index.html') else doc_name

    html_tree = html.fromstring(path.read_text())
    for element in html_tree.xpath('//a[@name]'):
        ids.add(f"{doc_name}#{element.get('name')}")
    for element in html_tree.xpath('//*[@id]'):
        ids.add(f"{doc_name}#{element.get('id')}")
    for element in html_tree.xpath('//a[@href]'):
        href = element.get('href')
        if href.startswith(('http', 'mailto')) or '#' not in href:
            continue
        if href.startswith('#'):
            href = f'{doc_name}{href}'
        if href.startswith('.'):
            href = f'/{path.parent.joinpath(href).resolve().relative_to(PUBLIC_DIR.absolute())}'
        links.append((doc_name, href))

broken = False
for doc_name, link in links:
    if link not in ids:
        print(f'[broken link] {doc_name} links to {link}')
        broken = True
if broken:
    sys.exit(1)
