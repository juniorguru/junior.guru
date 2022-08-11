import re
from pathlib import Path

from invoke import Exit, task
from lxml import html

from juniorguru.lib import loggers


logger = loggers.get(__name__)


PUBLIC_DIR = Path('public')

CLOUDINARY_URL = re.compile(r'.*https://junior\.guru')


@task(name='docs')
def main(context):
    links = []
    targets = set()
    images = set()

    for path in PUBLIC_DIR.glob('**/*.html'):
        logger.info(f'Reading {path}')
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
        for element in html_tree.cssselect('img[src]'):
            src = CLOUDINARY_URL.sub('', element.get('src'))
            if src.startswith(('http', 'mailto')):
                continue
            if src.startswith('/'):
                src = src.lstrip('/')
            elif src.startswith('.'):
                src = f'{path.parent.joinpath(src).resolve().relative_to(PUBLIC_DIR.absolute())}'
            images.add((doc_name, src))

    broken = False
    for doc_name, link in links:
        if link not in targets:
            logger.error(f'Broken link! {doc_name} links to {link}')
            broken = True
    for doc_name, image_path in images:
        image_path = PUBLIC_DIR / image_path
        if not image_path.exists():
            logger.error(f'Broken image! {doc_name} links to {image_path}')
            broken = True
    if broken:
        raise Exit(code=1)
    else:
        logger.info(f'Checked {len(links)} links, {len(targets)} targets, {len(images)} images. All good!')
