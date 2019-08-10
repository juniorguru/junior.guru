from pathlib import Path

from juniorguru.templates import render_template


template_path = Path(__file__).parent / 'template.html'
render_template('/', template_path, {})
