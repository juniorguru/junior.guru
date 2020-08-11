import sys
from pathlib import Path

import pytest


PROJECT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_DIR / 'scripts'
TEMPLATES_DIR = PROJECT_DIR / 'juniorguru' / 'web' / 'templates'


sys.path.append(str(SCRIPTS_DIR))
from generate_toc import main as generate_toc


@pytest.mark.parametrize('path,html', [
    pytest.param(path, contents, id=path.name) for path, contents in
    ((path, path.read_text()) for path in TEMPLATES_DIR.glob('*.html'))
    if 'id="toc"' in contents
])
def test_toc_is_in_sync_with_content(path, html):
    toc_html = generate_toc(path)
    assert toc_html in html
