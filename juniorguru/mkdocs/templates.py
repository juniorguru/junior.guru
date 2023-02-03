from collections import Counter
from pathlib import Path

import mkdocs_gen_files
from strictyaml import as_document

from juniorguru.lib import loggers
from juniorguru.models.partner import Partner


logger = loggers.from_path(__file__)


TEMPLATES_DIR = Path('juniorguru/mkdocs/docs-templates')

TEMPLATES = {}


def template(generate_pages):
    TEMPLATES[generate_pages.__name__] = generate_pages
    return generate_pages


@template
def generate_partner_pages():
    for partner in Partner.active_listing():
        yield dict(path=f'open/{partner.slug}.md',
                   meta=dict(title=f'Partnerství s firmou {partner.name}',
                             partner_slug=partner.slug,
                             noindex=True),
                   template='partner.md')


def main():
    logger.info('Generating pages')
    counter = Counter()
    for name, generate_pages in TEMPLATES.items():
        logger[name].debug('Generating')
        for page in generate_pages():
            path = page['path']
            yaml = as_document(page['meta']).as_yaml()
            markdown = (TEMPLATES_DIR / page['template']).read_text()
            content = f'---\n{yaml}\n---\n{markdown}'
            logger[name].debug(f'Writing {len(content)} characters to {path}')
            with mkdocs_gen_files.open(path, 'w') as f:
                f.write(content)
            counter[name] += 1
        level = 'info' if counter[name] else 'warning'
        getattr(logger[name], level)(f'Generated {counter[name]} pages')

if __name__ in ('__main__', '<run_path>'):
    main()
