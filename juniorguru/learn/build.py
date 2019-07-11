from pathlib import Path

from juniorguru.templating import render_template


data = dict(name='Honza')


template_path = Path(__file__).parent / 'template.html'
render_template('/learn/', template_path, data)
