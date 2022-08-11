from pathlib import Path

from invoke import Exit, task
from lxml import html

from juniorguru.lib import loggers


logger = loggers.get(__name__)


PUBLIC_DIR = Path('public')


@task(name='docs')
def main(context):
    links = []
    targets = set()

    for path in PUBLIC_DIR.glob('**/*.html'):
        logger.info(f'Reading {path}, so far found {len(links)} links and {len(targets)} targets')
        doc_name = f'/{path.relative_to(PUBLIC_DIR)}'
        doc_name = doc_name[:-10] if doc_name.endswith('index.html') else doc_name
        targets.add(doc_name)

        html_tree = html.fromstring(path.read_bytes())
        for element in html_tree.cssselect('a[name]'):
            targets.add(f"{doc_name}#{element.get('name')}")
        for element in html_tree.cssselect('*[id]'):
            targets.add(f"{doc_name}#{element.get('id')}")
        for element in html_tree.cssselect('a[href]'):
            href = element.get('href')
            if href.startswith(('http', 'mailto')):
                continue
            if href.startswith('#'):
                href = f'{doc_name}{href}'
            if not href.startswith(('.', '/')):
                href = f'./{href}'
            if href.startswith('.'):
                href = f'/{path.parent.joinpath(href).resolve().relative_to(PUBLIC_DIR.absolute())}'
            if not href.endswith('/') and '#' not in href:
                href = f'{href}/'
            if href == '/./':
                href = '/'
            links.append((doc_name, href))

    broken = False
    for doc_name, link in links:
        if link not in targets:
            logger.error(f'Broken link! {doc_name} links to {link}')
            broken = True
    if broken:
        raise Exit(code=1)
    else:
        logger.info(f'Checked {len(links)} links and {len(targets)} targets. All good!')
