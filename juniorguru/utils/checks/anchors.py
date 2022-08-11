# https://github.com/stevenvachon/broken-link-checker/issues/166

from pathlib import Path

from invoke import Exit, task
from lxml import html

from juniorguru.lib import loggers


logger = loggers.get(__name__)


PUBLIC_DIR = Path('public')


@task(name='anchors')
def main(context):
    links = []
    targets = set()

    for path in PUBLIC_DIR.glob('**/*.html'):
        logger.info(f'Reading {path}, so far found {len(links)} links and {len(targets)} targets')
        doc_name = f'/{path.relative_to(PUBLIC_DIR)}'
        doc_name = doc_name[:-10] if doc_name.endswith('index.html') else doc_name

        html_tree = html.fromstring(path.read_bytes())
        for element in html_tree.cssselect('a[name]'):
            name_target = f"{doc_name}#{element.get('name')}"
            logger.debug(f"{doc_name} has a name target: {name_target}")
            targets.add(name_target)
        for element in html_tree.cssselect('*[id]'):
            id_target = f"{doc_name}#{element.get('id')}"
            logger.debug(f"{doc_name} has an ID target: {id_target}")
            targets.add(id_target)
        for element in html_tree.cssselect('a[href]'):
            href = element.get('href')
            if href.startswith(('http', 'mailto')) or '#' not in href:
                continue
            if href.startswith('#'):
                href = f'{doc_name}{href}'
            if href.startswith('.'):
                href = f'/{path.parent.joinpath(href).resolve().relative_to(PUBLIC_DIR.absolute())}'
            logger.debug(f"{doc_name} links to: {href}")
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
